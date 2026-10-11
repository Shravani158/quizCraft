
import pytest

from quizcraft.file_reader import read_text_file


def test_reads_text_file(tmp_path):
    file_path = tmp_path / "notes.txt"
    file_path.write_text(
        "Natural Language Processing is useful.",
        encoding="utf-8",
    )

    result = read_text_file(str(file_path))

    assert result == "Natural Language Processing is useful."


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        read_text_file("missing_notes.txt")


def test_rejects_non_txt_file(tmp_path):
    file_path = tmp_path / "notes.pdf"
    file_path.write_text("dummy content", encoding="utf-8")

    with pytest.raises(ValueError):
        read_text_file(str(file_path))


def test_strips_outer_whitespace(tmp_path):
    file_path = tmp_path / "notes.txt"
    file_path.write_text(
        "   Python is useful.   ",
        encoding="utf-8",
    )

    assert read_text_file(str(file_path)) == "Python is useful."
