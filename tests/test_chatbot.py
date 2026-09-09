"""
test_chatbot.py - Unit Test Suite for CareerCompass Chatbot

Covers:
1. NLP Preprocessing: lowercasing, punctuation, stop-word removal, lemmatization
2. Exact Question Matching: high confidence matching on FAQ items
3. Paraphrased Questions: semantically equivalent questions with different phrasing
4. Case and Punctuation Insensitivity: UPPERCASE, symbols, and extra punctuation
5. Unrelated Questions: triggering the friendly fallback response
6. Empty and Whitespace Inputs: prompting the user to type a question
7. Threshold Sensitivity: behavior when similarity falls below configured threshold
"""

import os
import sys
import unittest

# Ensure the project root is on the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from chatbot import CareerCompassBot, DEFAULT_FALLBACK_MESSAGE
from nlp_processor import NLPProcessor, preprocess


class TestNLPProcessor(unittest.TestCase):
    """Unit tests for the NLTK preprocessing pipeline."""

    def setUp(self):
        self.processor = NLPProcessor()

    def test_lowercasing_and_punctuation(self):
        text = "Hello, World! How are you doing today???"
        cleaned = self.processor.clean_text(text)
        self.assertEqual(cleaned, "hello world how are you doing today")

    def test_domain_term_preservation(self):
        text = "Should I learn C++ or C# for .NET development?"
        cleaned = self.processor.clean_text(text)
        self.assertIn("cpp", cleaned)
        self.assertIn("csharp", cleaned)
        self.assertIn("dotnet", cleaned)

    def test_tokenization_and_stopwords(self):
        text = "How can I prepare for internships?"
        processed = preprocess(text)
        tokens = processed.split()
        self.assertNotIn("how", tokens)
        self.assertNotIn("can", tokens)
        self.assertNotIn("i", tokens)
        self.assertNotIn("for", tokens)
        self.assertIn("prepare", tokens)
        self.assertIn("internship", tokens)

    def test_lemmatization(self):
        # 'internships' -> 'internship', 'preparing' -> 'prepare', 'studies' -> 'study'
        tokens = ["internships", "preparing", "studies", "algorithms"]
        lemmas = self.processor.lemmatize_tokens(tokens)
        self.assertEqual(lemmas, ["internship", "prepare", "study", "algorithm"])

    def test_empty_string_preprocessing(self):
        self.assertEqual(preprocess(""), "")
        self.assertEqual(preprocess("   "), "")
        self.assertEqual(preprocess("???!!!"), "")


class TestCareerCompassBot(unittest.TestCase):
    """Unit tests for FAQ matching, ranking, and thresholding."""

    @classmethod
    def setUpClass(cls):
        # Use the real FAQ dataset in the repository
        cls.bot = CareerCompassBot(faq_path="faq_data.json", similarity_threshold=0.25)

    def test_exact_question_match(self):
        query = "How should I prepare for campus placements?"
        response = self.bot.get_response(query)
        self.assertFalse(response["fallback"])
        self.assertEqual(response["category"], "Placements")
        self.assertGreater(response["confidence"], 0.5)
        self.assertIn("programming fundamentals", response["answer"].lower())

    def test_paraphrased_questions_placement(self):
        # Different variations of placement questions should resolve to the same FAQ
        variations = [
            "How can I prepare for placements?",
            "What should I do to get ready for campus recruitment?",
            "How do I get ready for placement interviews?",
        ]
        for query in variations:
            with self.subTest(query=query):
                res = self.bot.get_response(query)
                self.assertFalse(res["fallback"], f"Failed for query: {query}")
                self.assertEqual(res["category"], "Placements")
                self.assertGreaterEqual(res["confidence"], 0.25)

    def test_machine_learning_query(self):
        query = "I want to become an AI engineer. What should I learn?"
        response = self.bot.get_response(query)
        self.assertFalse(response["fallback"])
        self.assertEqual(response["category"], "AI/ML")
        self.assertGreaterEqual(response["confidence"], 0.4)

    def test_internship_query(self):
        query = "How do I get an internship?"
        response = self.bot.get_response(query)
        self.assertFalse(response["fallback"])
        self.assertEqual(response["category"], "Internships")
        self.assertGreaterEqual(response["confidence"], 0.3)

    def test_resume_query(self):
        query = "How do I make a resume?"
        response = self.bot.get_response(query)
        self.assertFalse(response["fallback"])
        self.assertEqual(response["category"], "Resume")
        self.assertGreaterEqual(response["confidence"], 0.3)

    def test_ece_student_python_query(self):
        query = "Should an ECE student learn Python?"
        response = self.bot.get_response(query)
        self.assertFalse(response["fallback"])
        self.assertEqual(response["category"], "ECE Careers")
        self.assertGreater(response["confidence"], 0.6)

    def test_uppercase_and_punctuation_variation(self):
        query = "HOW CAN I PREPARE FOR CAMPUS PLACEMENTS???!!!"
        response = self.bot.get_response(query)
        self.assertFalse(response["fallback"])
        self.assertEqual(response["category"], "Placements")

    def test_empty_and_whitespace_input(self):
        res1 = self.bot.get_response("")
        self.assertTrue(res1["fallback"])
        self.assertEqual(res1["answer"], "Please type a question first.")

        res2 = self.bot.get_response("    ")
        self.assertTrue(res2["fallback"])
        self.assertEqual(res2["answer"], "Please type a question first.")

    def test_unrelated_query_triggers_fallback(self):
        unrelated = "What is the recipe for baking a chocolate cake?"
        response = self.bot.get_response(unrelated)
        self.assertTrue(response["fallback"])
        self.assertEqual(response["answer"], DEFAULT_FALLBACK_MESSAGE)
        self.assertLess(response["confidence"], 0.25)

    def test_threshold_sensitivity(self):
        # Instantiating a bot with high threshold should reject borderline queries
        strict_bot = CareerCompassBot(faq_path="faq_data.json", similarity_threshold=0.95)
        response = strict_bot.get_response("Tell me about placements")
        # Unless exact match with near 1.0 score, should trigger fallback
        self.assertTrue(response["fallback"])
        self.assertEqual(response["answer"], DEFAULT_FALLBACK_MESSAGE)

    def test_categories_available(self):
        categories = self.bot.get_categories()
        expected = [
            "AI/ML", "Career Paths", "Certifications", "ECE Careers",
            "Higher Studies", "Internships", "Placements", "Programming", "Projects", "Resume"
        ]
        for cat in expected:
            self.assertIn(cat, categories)


if __name__ == "__main__":
    unittest.main()
