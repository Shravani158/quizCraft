
import re

from quizcraft.question_generator import nlp


def score_question(question: str, answer: str) -> dict:
    """
    Estimate question difficulty using spaCy NLP features.
    This is a rule-based estimate, not a trained ML model.
    """

    # Remove the blank marker before analyzing the sentence.
    cleaned_question = re.sub(r"_+", " ", question)
    doc = nlp(cleaned_question)

    # Count meaningful words.
    content_words = [
        token
        for token in doc
        if token.is_alpha and not token.is_stop
    ]

    # Identify longer words.
    long_words = [
        token
        for token in content_words
        if len(token.text) >= 8
    ]

    # Estimate grammatical complexity.
    max_depth = max(
        (len(list(token.ancestors)) for token in doc),
        default=0,
    )

    score = 0

    if len(content_words) >= 12:
        score += 1

    if len(content_words) >= 20:
        score += 1

    if len(long_words) >= 2:
        score += 1

    if len(answer.strip()) >= 8:
        score += 1

    if max_depth >= 4:
        score += 1

    if score <= 1:
        difficulty = "Easy"
    elif score <= 3:
        difficulty = "Medium"
    else:
        difficulty = "Hard"

    return {
        "difficulty": difficulty,
        "difficulty_score": score,
    }


def rank_questions(questions: list[dict]) -> list[dict]:
    """Rank questions from highest difficulty score to lowest."""

    ranked_questions = []

    for question in questions:
        result = score_question(
            question["question"],
            question["answer"],
        )

        ranked_item = {
            **question,
            **result,
        }

        ranked_questions.append(ranked_item)

    return sorted(
        ranked_questions,
        key=lambda item: item["difficulty_score"],
        reverse=True,
    )
