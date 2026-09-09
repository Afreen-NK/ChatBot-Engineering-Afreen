"""
chatbot.py - Core Matching Engine for CareerCompass

This module implements FAQ retrieval using:
1. NLTK-based text preprocessing (from nlp_processor.py)
2. Scikit-learn TfidfVectorizer (unigram + bigram)
3. Cosine similarity matching against the FAQ vector space
4. Configurable thresholding and student-friendly fallbacks
5. Explainable console logging for college viva/demonstrations
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nlp_processor import preprocess

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("CareerCompassBot")

# Configurable default threshold
DEFAULT_SIMILARITY_THRESHOLD = 0.25

DEFAULT_FALLBACK_MESSAGE = (
    "I'm not sure I understood that question. Try asking about internships, "
    "placements, resumes, projects, programming, AI/ML, or career paths."
)


class CareerCompassBot:
    """
    CareerCompass FAQ Chatbot Engine.
    Precomputes TF-IDF representations of FAQ questions and keywords,
    and resolves user questions via cosine similarity.
    """

    def __init__(
        self,
        faq_path: str = "faq_data.json",
        similarity_threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
    ):
        self.faq_path = faq_path
        self.similarity_threshold = similarity_threshold
        self.faqs: List[Dict[str, Any]] = []
        self.corpus: List[str] = []
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.tfidf_matrix = None

        self.load_dataset()
        self.build_model()

    def load_dataset(self) -> None:
        """Loads FAQ dataset from JSON file."""
        if not os.path.exists(self.faq_path):
            raise FileNotFoundError(f"FAQ dataset file not found at: {self.faq_path}")

        with open(self.faq_path, "r", encoding="utf-8") as f:
            self.faqs = json.load(f)

        if not isinstance(self.faqs, list) or len(self.faqs) == 0:
            raise ValueError(f"FAQ dataset at {self.faq_path} is empty or invalid.")

        logger.info(f"Loaded {len(self.faqs)} FAQs across {len(self.get_categories())} categories.")

    def build_model(self) -> None:
        """
        Preprocesses FAQ questions and keywords, and trains the TF-IDF Vectorizer.
        N-gram range (1, 2) is used to capture important engineering phrases
        (e.g., 'machine learning', 'data structures', 'campus placements').
        """
        self.corpus = []
        for item in self.faqs:
            question = item.get("question", "")
            keywords = " ".join(item.get("keywords", []))
            # Combine question and keywords for a rich lexical representation
            raw_text = f"{question} {keywords}"
            processed = preprocess(raw_text)
            self.corpus.append(processed)

        # Build TF-IDF Vectorizer with unigrams and bigrams
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)
        self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)
        logger.info(
            f"TF-IDF model built successfully. Vocabulary size: {len(self.vectorizer.vocabulary_)} terms."
        )

    def get_categories(self) -> List[str]:
        """Returns sorted list of unique FAQ categories."""
        categories = sorted(list(set(item["category"] for item in self.faqs if "category" in item)))
        return categories

    def get_faqs_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Returns all FAQs belonging to a specific category."""
        return [item for item in self.faqs if item.get("category", "").lower() == category.lower()]

    def get_response(self, user_query: str, top_k: int = 3) -> Dict[str, Any]:
        """
        Processes a user question and returns the best matching FAQ response.

        Args:
            user_query: Raw user question string.
            top_k: Number of top candidate matches to inspect internally.

        Returns:
            Dict containing answer, confidence score, matched_question, category,
            fallback flag, and explainable top candidates.
        """
        # 1. Validate empty or whitespace input
        if not user_query or not user_query.strip():
            return {
                "answer": "Please type a question first.",
                "confidence": 0.0,
                "matched_question": None,
                "category": None,
                "fallback": True,
                "top_matches": [],
            }

        # 2. Preprocess user query using NLTK pipeline
        processed_query = preprocess(user_query)

        # Handle queries that collapse to empty (e.g. only punctuation or stop-words)
        if not processed_query.strip():
            logger.warning(f"Query '{user_query}' yielded empty preprocessed text.")
            return {
                "answer": DEFAULT_FALLBACK_MESSAGE,
                "confidence": 0.0,
                "matched_question": None,
                "category": None,
                "fallback": True,
                "top_matches": [],
            }

        # 3. Vectorize user query into TF-IDF space
        query_vector = self.vectorizer.transform([processed_query])

        # 4. Compute cosine similarity against all FAQ vectors
        similarity_scores = cosine_similarity(query_vector, self.tfidf_matrix)[0]

        # 5. Rank matches in descending order of similarity
        ranked_indices = similarity_scores.argsort()[::-1]

        top_matches = []
        for i in range(min(top_k, len(ranked_indices))):
            idx = int(ranked_indices[i])
            score = float(similarity_scores[idx])
            top_matches.append({
                "id": self.faqs[idx].get("id"),
                "question": self.faqs[idx].get("question"),
                "category": self.faqs[idx].get("category"),
                "score": round(score, 4),
            })

        best_idx = int(ranked_indices[0])
        best_score = float(similarity_scores[best_idx])
        best_faq = self.faqs[best_idx]

        # 6. Log explainable data to console for viva / demonstration
        print("\n" + "=" * 60)
        print("[CareerCompass NLP Matcher]")
        print(f"  User Query       : {user_query}")
        print(f"  Processed Query  : {processed_query}")
        print(f"  Top Matched FAQ  : {best_faq['question']}")
        print(f"  Category         : {best_faq['category']}")
        print(f"  Cosine Score     : {best_score:.4f} (Threshold: {self.similarity_threshold})")
        print(f"  Match Status     : {'SUCCESS' if best_score >= self.similarity_threshold else 'FALLBACK'}")
        print("=" * 60 + "\n")

        # 7. Check similarity threshold
        if best_score < self.similarity_threshold:
            return {
                "answer": DEFAULT_FALLBACK_MESSAGE,
                "confidence": round(best_score, 4),
                "matched_question": None,
                "category": None,
                "fallback": True,
                "top_matches": top_matches,
            }

        # 8. Return successful match
        return {
            "answer": best_faq.get("answer", ""),
            "confidence": round(best_score, 4),
            "matched_question": best_faq.get("question"),
            "category": best_faq.get("category"),
            "id": best_faq.get("id"),
            "fallback": False,
            "top_matches": top_matches,
        }
