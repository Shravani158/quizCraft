
from quizcraft.question_generator import generate_fill_blank_questions


def test_generates_questions():
    text = (
        "Tokenization is the process of splitting text "
        "into smaller units called tokens."
    )

    questions = generate_fill_blank_questions(text)

    assert len(questions) > 0


def test_question_contains_blank():
    text = (
        "Tokenization is the process of splitting text "
        "into smaller units called tokens."
    )

    questions = generate_fill_blank_questions(text)

    assert any(
        "________" in item["question"]
        for item in questions
    )


def test_question_has_answer():
    text = (
        "Tokenization is the process of splitting text "
        "into smaller units called tokens."
    )

    questions = generate_fill_blank_questions(text)

    assert all(
        item["answer"].strip()
        for item in questions
    )


def test_empty_input():
    assert generate_fill_blank_questions("") == []
