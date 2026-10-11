
from quizcraft.difficulty import score_question, rank_questions


def test_score_question_returns_expected_fields():
    result = score_question(
        "Python is a programming language.",
        "language",
    )

    assert "difficulty" in result
    assert "difficulty_score" in result
    assert result["difficulty"] in {"Easy", "Medium", "Hard"}
    assert 0 <= result["difficulty_score"] <= 5


def test_short_simple_question_is_easy():
    result = score_question(
        "Python is useful.",
        "Python",
    )

    assert result["difficulty"] == "Easy"


def test_rank_questions_orders_highest_score_first():
    questions = [
        {
            "question": "Python is useful.",
            "answer": "Python",
        },
        {
            "question": (
                "Natural language processing enables computers "
                "to understand complex human communication patterns."
            ),
            "answer": "communication",
        },
    ]

    ranked = rank_questions(questions)

    scores = [
        item["difficulty_score"]
        for item in ranked
    ]

    assert scores == sorted(scores, reverse=True)


def test_rank_questions_does_not_modify_original():
    questions = [
        {
            "question": "Python is useful.",
            "answer": "Python",
        }
    ]

    original = questions[0].copy()
    rank_questions(questions)

    assert questions[0] == original
