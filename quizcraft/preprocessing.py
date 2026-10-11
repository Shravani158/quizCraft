
import re
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


def download_nltk_resources():
    """Download the language data required by NLTK."""
    nltk.download("punkt_tab", quiet=True)
    nltk.download("stopwords", quiet=True)


def clean_text(text: str) -> str:
    """Remove URLs and normalize whitespace."""

    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def split_sentences(text: str) -> list[str]:
    """Split study material into individual sentences."""

    cleaned_text = clean_text(text)

    if not cleaned_text:
        return []

    return sent_tokenize(cleaned_text)


def tokenize_text(text: str) -> list[str]:
    """Split text into individual alphabetic words."""

    tokens = word_tokenize(text)

    return [
        token.lower()
        for token in tokens
        if token.isalpha()
    ]


def remove_stopwords(tokens: list[str]) -> list[str]:
    """Remove common words while preserving negations."""

    stop_words = set(stopwords.words("english"))

    # Keep words that can change the meaning of a sentence.
    stop_words.difference_update({"no", "nor", "not", "never"})

    return [
        word
        for word in tokens
        if word.lower() not in stop_words
    ]


if __name__ == "__main__":
    download_nltk_resources()
    print("NLTK resources are ready.")
