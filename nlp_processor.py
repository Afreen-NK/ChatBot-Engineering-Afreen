"""
nlp_processor.py - Natural Language Processing Pipeline for CareerCompass

This module implements classical text preprocessing techniques using NLTK:
1. Text normalization & lowercasing
2. Domain-specific token preservation (e.g., C++ -> cpp, C# -> csharp)
3. Punctuation removal
4. Tokenization using NLTK word_tokenize (with regex fallback)
5. Stop-word removal using NLTK stopwords
6. Lemmatization using WordNetLemmatizer (dual-pass verb & noun)
"""

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def ensure_nltk_resources():
    """
    Ensures that required NLTK corpora and tokenizer models are downloaded.
    Fails gracefully if offline, falling back to local copies if present.
    """
    required_packages = [
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab"),
        ("corpora/stopwords", "stopwords"),
        ("corpora/wordnet", "wordnet"),
        ("corpora/omw-1.4", "omw-1.4"),
    ]
    for path, pkg_name in required_packages:
        try:
            nltk.data.find(path)
        except (LookupError, AttributeError):
            try:
                nltk.download(pkg_name, quiet=True)
            except Exception as e:
                print(f"[Warning] Could not download NLTK resource '{pkg_name}': {e}")


# Initialize resources on module import
ensure_nltk_resources()


class NLPProcessor:
    """
    Reusable Natural Language Preprocessing class.
    Converts raw user and FAQ questions into canonical lemmatized token strings.
    """

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        try:
            self.stop_words = set(stopwords.words("english"))
        except Exception:
            # Safe minimal fallback in case NLTK stopwords cannot load
            self.stop_words = {
                "a", "about", "above", "after", "again", "against", "all", "am", "an",
                "and", "any", "are", "aren't", "as", "at", "be", "because", "been",
                "before", "being", "below", "between", "both", "but", "by", "can",
                "cannot", "could", "did", "do", "does", "doing", "don't", "down",
                "during", "each", "few", "for", "from", "further", "had", "has",
                "have", "having", "he", "her", "here", "hers", "herself", "him",
                "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its",
                "itself", "me", "more", "most", "my", "myself", "no", "nor", "not",
                "of", "off", "on", "once", "only", "or", "other", "ought", "our",
                "ours", "ourselves", "out", "over", "own", "same", "she", "should",
                "so", "some", "such", "than", "that", "the", "their", "theirs", "them",
                "themselves", "then", "there", "these", "they", "this", "those",
                "through", "to", "too", "under", "until", "up", "very", "was", "we",
                "were", "what", "when", "where", "which", "while", "who", "whom",
                "why", "with", "would", "you", "your", "yours", "yourself"
            }

    def normalize_domain_terms(self, text: str) -> str:
        """
        Preserve key engineering terms that contain punctuation before stripping.
        E.g., C++ -> cpp, C# -> csharp, .NET -> dotnet, AI/ML -> ai ml.
        """
        text = re.sub(r"(?i)\bc\+\+", "cpp", text)
        text = re.sub(r"(?i)\bc\#", "csharp", text)
        text = re.sub(r"(?i)\.net\b", "dotnet", text)
        text = text.replace("/", " ").replace("\\", " ")
        return text

    def clean_text(self, text: str) -> str:
        """
        1. Converts text to lowercase.
        2. Normalizes domain terms (C++, C#, AI/ML).
        3. Replaces punctuation with spaces.
        4. Strips redundant whitespace.
        """
        if not text:
            return ""

        text = text.lower()
        text = self.normalize_domain_terms(text)

        # Replace punctuation characters with spaces to preserve word boundaries
        translation_table = str.maketrans({char: " " for char in string.punctuation})
        text = text.translate(translation_table)

        # Collapse repeated whitespace
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def tokenize(self, text: str) -> list[str]:
        """
        Tokenizes cleaned text using NLTK word_tokenize with regex fallback.
        """
        if not text:
            return []
        try:
            tokens = word_tokenize(text)
        except Exception:
            # Fallback regex tokenizer if NLTK punkt is unavailable
            tokens = re.findall(r"\b[a-zA-Z0-9]+\b", text)
        return tokens

    def remove_stopwords(self, tokens: list[str]) -> list[str]:
        """
        Filters out common English stop words while keeping informative content tokens.
        """
        return [token for token in tokens if token not in self.stop_words and len(token) > 1]

    def lemmatize_tokens(self, tokens: list[str]) -> list[str]:
        """
        Lemmatizes tokens to their dictionary root form using WordNetLemmatizer.
        Applies verb lemmatization followed by noun lemmatization to handle
        words like 'preparing' -> 'prepare' and 'internships' -> 'internship'.
        """
        lemmatized = []
        for token in tokens:
            # First reduce verb inflection (e.g. 'preparing' -> 'prepare')
            lemma = self.lemmatizer.lemmatize(token, pos="v")
            # Next reduce noun plurals (e.g. 'internships' -> 'internship')
            lemma = self.lemmatizer.lemmatize(lemma, pos="n")
            lemmatized.append(lemma)
        return lemmatized

    def preprocess(self, text: str) -> str:
        """
        Complete NLP pipeline:
        Raw text -> Lowercase & clean -> Tokenize -> Remove stop words -> Lemmatize -> Processed string
        
        Example:
            Input: "How can I prepare for AI/ML internships?"
            Output: "prepare ai ml internship"
        """
        cleaned = self.clean_text(text)
        if not cleaned:
            return ""

        tokens = self.tokenize(cleaned)
        filtered_tokens = self.remove_stopwords(tokens)
        lemmas = self.lemmatize_tokens(filtered_tokens)

        return " ".join(lemmas)


# Global singleton instance for easy import across modules
_nlp_instance = NLPProcessor()


def preprocess(text: str) -> str:
    """Convenience helper function to preprocess text using the global NLPProcessor instance."""
    return _nlp_instance.preprocess(text)
