import spacy

from quizcraft.preprocessing import split_sentences


# Load the English NLP model once.
nlp = spacy.load("en_core_web_sm")


def generate_fill_blank_questions(text: str) -> list[dict]:
    """Generate fill-in-the-blank questions using noun identification."""

    sentences = split_sentences(text)
    questions = []

    for sentence in sentences:
        doc = nlp(sentence)

        # Find nouns and proper nouns.
        candidates = [
            token
            for token in doc
            if token.pos_ in {"NOUN", "PROPN"}
            and not token.is_stop
            and token.is_alpha
        ]

        # Skip sentences without a suitable candidate.
        if not candidates:
            continue

        # Prefer proper nouns, then longer words.
        answer_token = max(
            candidates,
            key=lambda token: (
                token.pos_ == "PROPN",
                len(token.text),
            ),
        )

        answer = answer_token.text

        # Replace the selected word while preserving punctuation.
        start = answer_token.idx
        end = start + len(answer_token.text)

        question_text = (
            sentence[:start]
            + "________"
            + sentence[end:]
        )

        questions.append({
            "question": question_text,
            "answer": answer
        })

    return questions


if __name__ == "__main__":
    sample_text = """
    Natural Language Processing is a branch of Artificial Intelligence.
    Tokenization is the process of splitting text into smaller units called tokens.
    Stemming reduces words to their root forms.
    """

    generated_questions = generate_fill_blank_questions(sample_text)

    for index, item in enumerate(generated_questions, start=1):
        print(f"Q{index}. {item['question']}")
        print(f"Answer: {item['answer']}")
        print()