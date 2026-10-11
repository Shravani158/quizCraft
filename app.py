
from pathlib import Path
import re
import string

import streamlit as st

from quizcraft.question_generator import generate_fill_blank_questions
from quizcraft.mcq_generator import generate_mcqs
from quizcraft.difficulty import rank_questions


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="QuizCraft | Smart Study",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------- CUSTOM STYLING ----------------

css_path = Path(__file__).parent / "style.css"

if css_path.exists():
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )


# ---------------- HELPER FUNCTIONS ----------------

def extract_text(uploaded_file):
    """Extract text from an uploaded TXT or PDF file."""

    if uploaded_file.name.lower().endswith(".pdf"):
        import pymupdf

        with pymupdf.open(
            stream=uploaded_file.getvalue(),
            filetype="pdf",
        ) as document:
            return "\n".join(
                page.get_text()
                for page in document
            ).strip()

    return uploaded_file.getvalue().decode("utf-8").strip()


def filter_by_difficulty(questions, difficulty):
    """Keep questions matching the selected difficulty."""

    if difficulty == "Any":
        return questions

    return [
        question
        for question in questions
        if question["difficulty"] == difficulty
    ]


def normalize_answer(answer):
    """Normalize answers so capitalization and punctuation do not matter."""

    answer = answer.casefold().strip()
    answer = answer.translate(
        str.maketrans("", "", string.punctuation)
    )
    return re.sub(r"\s+", " ", answer)


def prepare_download(fill_blank, mcqs):
    """Prepare questions and answers for a text download."""

    lines = ["QUIZCRAFT - GENERATED QUESTIONS\n"]

    for index, item in enumerate(fill_blank, start=1):
        lines.extend([
            f"\nFill in the blank {index}:",
            item["question"],
            f"Difficulty: {item['difficulty']}",
            f"Answer: {item['answer']}",
        ])

    for index, item in enumerate(mcqs, start=1):
        lines.extend([
            f"\nMCQ {index}:",
            item["question"],
            f"Difficulty: {item['difficulty']}",
        ])

        lines.extend(
            f"{chr(65 + i)}. {option}"
            for i, option in enumerate(item["options"])
        )

        lines.append(f"Answer: {item['answer']}")

    return "\n".join(lines)


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.title("📚 QuizCraft")
    st.caption("Your personal study companion")

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload your study material",
        type=["txt", "pdf"],
        help="Upload a text file or a text-readable PDF.",
    )

    st.subheader("⚙️ Quiz settings")

    # Only one question type can be selected.
    question_type = st.radio(
        "Choose your quiz type",
        [
            "Fill in the blanks",
            "Multiple-choice questions",
        ],
    )

    num_questions = st.number_input(
        "Number of questions",
        min_value=1,
        max_value=50,
        value=10,
        step=1,
    )

    difficulty_preference = st.selectbox(
        "Difficulty",
        ["Any", "Easy", "Medium", "Hard"],
    )

    generate_clicked = st.button(
        "✨ Generate my quiz",
        type="primary",
        use_container_width=True,
    )

    st.divider()

    st.caption(
        "Tip: Use clear, text-based study notes for better results."
    )


# ---------------- GENERATE QUIZ ----------------

if generate_clicked:
    if uploaded_file is None:
        st.session_state["generation_error"] = (
            "Please upload a PDF or TXT file first."
        )
    else:
        try:
            with st.spinner("Reading your notes and creating questions..."):
                text = extract_text(uploaded_file)

                if not text:
                    raise ValueError(
                        "No readable text was found in this document."
                    )

                # Generate only the question type selected by the user.
                if question_type == "Fill in the blanks":
                    fill_blank = generate_fill_blank_questions(text)
                    mcqs = []
                else:
                    fill_blank = []
                    mcqs = generate_mcqs(text)

                # Estimate and rank difficulty.
                fill_blank = rank_questions(fill_blank)
                mcqs = rank_questions(mcqs)

                # Apply difficulty filter.
                fill_blank = filter_by_difficulty(
                    fill_blank,
                    difficulty_preference,
                )
                mcqs = filter_by_difficulty(
                    mcqs,
                    difficulty_preference,
                )

                # Apply question limit.
                st.session_state["fill_blank"] = (
                    fill_blank[:int(num_questions)]
                )
                st.session_state["mcqs"] = (
                    mcqs[:int(num_questions)]
                )

                st.session_state["study_text"] = text
                st.session_state["source_name"] = uploaded_file.name
                st.session_state["active_question_type"] = question_type
                st.session_state["selected_difficulty"] = (
                    difficulty_preference
                )

                st.session_state["quiz_attempt"] = (
                    st.session_state.get("quiz_attempt", 0) + 1
                )

                # Clear previous quiz results.
                st.session_state["quiz_submitted"] = False
                st.session_state["quiz_results"] = None
                st.session_state["quiz_score"] = 0
                st.session_state["quiz_validation_error"] = None
                st.session_state["generation_error"] = None

        except Exception as error:
            st.session_state["generation_error"] = str(error)


# ---------------- MAIN PAGE HEADER ----------------

st.markdown(
    """
    <div class="hero-card">
        <div class="eyebrow">LEARN • PRACTISE • IMPROVE</div>
        <h1>Your notes. Your quiz. Your progress.</h1>
        <p>
            Turn your study material into a quiz,
            test your knowledge, and track your score.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.session_state.get("generation_error"):
    st.error(st.session_state["generation_error"])

if "study_text" not in st.session_state:
    st.markdown(
        """
        <div class="section-card">
            <h3>👋 Welcome to QuizCraft</h3>
            <p>
                Upload your study notes using the sidebar.
                Choose either Fill in the Blanks or MCQs,
                and click <b>Generate my quiz</b>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "QuizCraft supports text-readable PDFs and UTF-8 TXT files."
    )


# ---------------- DISPLAY GENERATED QUIZ ----------------

if "study_text" in st.session_state:
    fill_blank = st.session_state.get("fill_blank", [])
    mcqs = st.session_state.get("mcqs", [])

    question_type = st.session_state["active_question_type"]
    questions = fill_blank if question_type == "Fill in the blanks" else mcqs

    total_questions = len(questions)

    st.caption(
        f"📄 Source: {st.session_state.get('source_name', 'Study material')}"
        f"  •  📝 Type: {question_type}"
        f"  •  🎯 Difficulty: "
        f"{st.session_state.get('selected_difficulty', 'Any')}"
    )

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric("Total questions", total_questions)
    metric2.metric("Question type", "Fill in Blanks" if question_type == "Fill in the blanks" else "MCQs")
    quiz_is_submitted = st.session_state.get("quiz_submitted", False)

    metric3.metric(
       "Submission status",
       "Submitted" if quiz_is_submitted else "Not submitted",
)

    if total_questions == 0:
        st.warning(
            "No questions were generated for these settings. "
            "Try choosing Any difficulty or uploading longer study notes."
        )

    quiz_tab, study_tab, results_tab = st.tabs(
        [
            "📝 Take quiz",
            "📖 Study questions",
            "🏆 Results",
        ]
    )

    # ---------------- TAKE QUIZ ----------------

    with quiz_tab:
        st.subheader("Test your knowledge")

        if not questions:
            st.info(
                "No questions are available. Try generating a new quiz "
                "with different settings."
            )
        else:
            attempt = st.session_state["quiz_attempt"]

            st.write(
                f"Answer all {total_questions} questions, "
                "then submit to see your score."
            )

            with st.form(key=f"quiz_form_{attempt}"):
                user_answers = {}

                for index, item in enumerate(questions, start=1):
                    st.markdown(
                        f"**Question {index} of {total_questions}**"
                    )

                    st.write(item["question"])

                    st.caption(
                        f"{item['difficulty']} difficulty"
                        f" · Score {item['difficulty_score']}/5"
                    )

                    if question_type == "Fill in the blanks":
                        user_answers[index] = st.text_input(
                            f"Your answer for question {index}",
                            key=f"blank_answer_{attempt}_{index}",
                            placeholder="Type your answer here...",
                        )
                    else:
                        user_answers[index] = st.radio(
                            f"Choose your answer for question {index}",
                            item["options"],
                            index=None,
                            key=f"mcq_answer_{attempt}_{index}",
                        )

                    st.divider()

                submitted = st.form_submit_button(
                    "Submit quiz",
                    type="primary",
                    use_container_width=True,
                )

            if submitted:
                unanswered = [
                    index
                    for index, answer in user_answers.items()
                    if answer is None or not str(answer).strip()
                ]

                if unanswered:
                    st.session_state["quiz_validation_error"] = (
                        f"You have {len(unanswered)} unanswered question(s). "
                        "Please answer every question before submitting."
                    )
                else:
                    results = []
                    score = 0

                    for index, item in enumerate(questions, start=1):
                        selected = str(user_answers[index]).strip()
                        correct_answer = item["answer"]

                        is_correct = (
                            normalize_answer(selected)
                            == normalize_answer(correct_answer)
                        )

                        if is_correct:
                            score += 1

                        results.append({
                            "question": item["question"],
                            "selected": selected,
                            "correct_answer": correct_answer,
                            "is_correct": is_correct,
                        })

                    st.session_state["quiz_results"] = results
                    st.session_state["quiz_score"] = score
                    st.session_state["quiz_submitted"] = True
                    st.session_state["quiz_validation_error"] = None

# Immediately refresh the page so the status and results update.
                    st.rerun()

            if st.session_state.get("quiz_validation_error"):
                st.warning(st.session_state["quiz_validation_error"])

            if st.session_state.get("quiz_submitted", False):
                st.success(
                    "Quiz submitted successfully! "
                    "Open the Results tab to see your score."
                )

    # ---------------- STUDY QUESTIONS ----------------

    with study_tab:
        st.subheader("Review your questions")

        if questions:
            for index, item in enumerate(questions, start=1):
                heading = (
                    f"Fill in the blank {index}"
                    if question_type == "Fill in the blanks"
                    else f"MCQ {index}"
                )

                with st.expander(heading):
                    st.write(item["question"])

                    if question_type == "Multiple-choice questions":
                        for option_index, option in enumerate(item["options"]):
                            st.write(
                                f"{chr(65 + option_index)}. {option}"
                            )

                    st.caption(
                        f"Difficulty: {item['difficulty']} "
                        f"({item['difficulty_score']}/5)"
                    )

            st.caption(
                "Answers stay hidden here. Submit the quiz to see "
                "the correct answers in Results."
            )
        else:
            st.info("Generate questions to see them here.")

    
    # ---------------- RESULTS DASHBOARD ----------------

    with results_tab:
        st.subheader("Your performance")

        if not st.session_state.get("quiz_submitted", False):
            st.markdown(
                '<div class="status-pending">⏳ Quiz not submitted</div>',
                unsafe_allow_html=True,
            )

            st.info(
                "Complete all questions in the Take Quiz tab and "
                "submit your answers to unlock your results."
            )

        else:
            results = st.session_state["quiz_results"]
            score = st.session_state["quiz_score"]
            total = len(results)

            percentage = score / total * 100 if total else 0
            incorrect = total - score

            if percentage >= 80:
                message = "Excellent work! You have a strong understanding."
            elif percentage >= 50:
                message = "Good effort! Review your mistakes to improve."
            else:
                message = "Keep practising. Every attempt helps you improve."

            # Main score card
            st.markdown(
                f"""
                <div class="results-hero">
                    <div class="results-label">Quiz completed</div>
                    <div class="results-score">{score} / {total}</div>
                    <div class="results-message">{percentage:.1f}% accuracy</div>
                    <p class="results-message">{message}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="status-pill">✓ Submission successful</div>',
                unsafe_allow_html=True,
            )

            # Performance metrics
            col1, col2, col3 = st.columns(3)

            col1.metric("✅ Correct", score)
            col2.metric("❌ Incorrect", incorrect)
            col3.metric("🎯 Accuracy", f"{percentage:.1f}%")

            # Progress indicator
            st.markdown("### Your progress")

            st.progress(
                int(round(percentage)),
                text=f"{score} out of {total} answers correct",
            )

            # Answer review
            st.markdown("### Review your answers")
            st.caption(
                "Open any question below to see your answer "
                "and the correct answer."
            )

            for index, result in enumerate(results, start=1):
                if result["is_correct"]:
                    title = f"✅ Question {index} — Correct"
                else:
                    title = f"❌ Question {index} — Incorrect"

                with st.expander(title):
                    st.markdown("**Question**")
                    st.write(result["question"])

                    if result["is_correct"]:
                        st.success(
                            f"Your answer: {result['selected']}"
                        )
                    else:
                        st.error(
                            f"Your answer: {result['selected']}"
                        )
                        st.info(
                            f"Correct answer: "
                            f"{result['correct_answer']}"
                        )

            st.divider()

            st.caption(
                "Tip: Review incorrect answers, then generate "
                "another quiz to practise again."
            )
