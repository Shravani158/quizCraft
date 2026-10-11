
import pytest

from quizcraft.mcq_generator import generate_mcqs


SAMPLE_TEXT = """
Python is a programming language.
Java is used for software development.
Tokenization splits text into smaller units.
Stemming reduces words to their root forms.
Lemmatization converts words into dictionary forms.
Classification assigns data to categories.
"""


def test_mcqs_are_generated():
    questions = generate_mcqs(SAMPLE_TEXT)

    assert len(questions) > 0


def test_mcq_has_four_options():
    questions = generate_mcqs(SAMPLE_TEXT)

    assert all(len(item["options"]) == 4 for item in questions)


def test_correct_answer_is_an_option():
    questions = generate_mcqs(SAMPLE_TEXT)

    assert all(
        item["answer"] in item["options"]
        for item in questions
    )


def test_options_are_distinct():
    questions = generate_mcqs(SAMPLE_TEXT)

    assert all(
        len(set(option.lower() for option in item["options"])) == 4
        for item in questions
    )


def test_invalid_number_of_options():
    with pytest.raises(ValueError):
        generate_mcqs(SAMPLE_TEXT, num_options=1)


def test_empty_input():
    assert generate_mcqs("") == []
