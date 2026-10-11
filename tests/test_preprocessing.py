
from quizcraft.preprocessing import (
    clean_text,
    split_sentences,
    tokenize_text,
)


def test_clean_text_removes_urls():
    text = "Read NLP notes at https://example.com"
    result = clean_text(text)

    assert "https://example.com" not in result
    assert "NLP notes" in result


def test_split_sentences():
    text = "NLP is useful. Tokenization splits text."
    result = split_sentences(text)

    assert len(result) == 2


def test_tokenize_text():
    result = tokenize_text("NLP uses tokens!")

    assert result == ["nlp", "uses", "tokens"]


def test_empty_text():
    assert split_sentences("") == []

