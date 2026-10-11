
from pathlib import Path

from quizcraft.file_reader import read_text_file
from quizcraft.pdf_reader import read_pdf_file
from quizcraft.question_generator import generate_fill_blank_questions
from quizcraft.mcq_generator import generate_mcqs


def generate_quiz(file_path: str) -> dict:
    """Read study material and generate both question types."""

    path = Path(file_path)

    if path.suffix.lower() == ".pdf":
        text = read_pdf_file(str(path))
    elif path.suffix.lower() == ".txt":
        text = read_text_file(str(path))
    else:
        raise ValueError("Please provide a .txt or .pdf file.")

    if not text.strip():
        raise ValueError(
            "No readable text was found in this document."
        )

    return {
        "fill_blank": generate_fill_blank_questions(text),
        "mcqs": generate_mcqs(text),
    }


if __name__ == "__main__":
    file_path = input(
        "Enter your study file path (.txt or .pdf): "
    ).strip().strip('"')

    try:
        quiz = generate_quiz(file_path)

        print("\n===== FILL-IN-THE-BLANK QUESTIONS =====")

        for index, item in enumerate(quiz["fill_blank"], start=1):
            print(f"\nQ{index}. {item['question']}")
            print(f"Answer: {item['answer']}")

        print("\n===== MULTIPLE-CHOICE QUESTIONS =====")

        for index, item in enumerate(quiz["mcqs"], start=1):
            print(f"\nQ{index}. {item['question']}")

            for option_index, option in enumerate(item["options"]):
                print(f"  {chr(65 + option_index)}. {option}")

            print(f"Answer: {item['answer']}")

        if not quiz["fill_blank"] and not quiz["mcqs"]:
            print(
                "\nNo questions could be generated. "
                "Try a document with more descriptive sentences."
            )

    except (ValueError, FileNotFoundError) as error:
        print(f"\nError: {error}")
