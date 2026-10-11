
import random

from quizcraft.question_generator import (
    generate_fill_blank_questions,
)


def generate_mcqs(text: str, num_options: int = 4) -> list[dict]:
    """Generate MCQs with distinct answer options."""

    if num_options < 2:
        raise ValueError("num_options must be at least 2.")

    fill_blank_questions = generate_fill_blank_questions(text)

    # Collect unique answers, ignoring differences in capitalization.
    all_answers = []
    seen_answers = set()

    for item in fill_blank_questions:
        answer = item["answer"].strip()
        normalized_answer = answer.casefold()

        if normalized_answer and normalized_answer not in seen_answers:
            all_answers.append(answer)
            seen_answers.add(normalized_answer)

    mcqs = []

    for item in fill_blank_questions:
        answer = item["answer"].strip()
        normalized_answer = answer.casefold()

        # Exclude the correct answer from the distractors.
        distractors = [
            word
            for word in all_answers
            if word.casefold() != normalized_answer
        ]

        # Skip if there are not enough distinct distractors.
        if len(distractors) < num_options - 1:
            continue

        selected_distractors = random.sample(
            distractors,
            num_options - 1,
        )

        # Add the correct answer exactly once.
        options = selected_distractors + [answer]
        random.shuffle(options)

        mcqs.append({
            "question": item["question"].replace(
                "________", "______"
            ),
            "options": options,
            "answer": answer,
        })

    return mcqs


if __name__ == "__main__":
    sample_text = """
    Python is a programming language.
    Java is used for software development.
    Tokenization splits text into smaller units.
    Stemming reduces words to their root forms.
    Lemmatization converts words into dictionary forms.
    Classification assigns data to categories.
    """

    questions = generate_mcqs(sample_text)

    for index, item in enumerate(questions, start=1):
        print(f"\nQ{index}. {item['question']}")

        for option_index, option in enumerate(item["options"]):
            label = chr(65 + option_index)
            print(f"  {label}. {option}")

        print(f"Answer: {item['answer']}")
