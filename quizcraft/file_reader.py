
from pathlib import Path


def read_text_file(file_path: str) -> str:
    """Read UTF-8 study material from a text file."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Study material not found: {path}"
        )

    if path.suffix.lower() != ".txt":
        raise ValueError("Only .txt files are supported currently.")

    return path.read_text(encoding="utf-8").strip()


if __name__ == "__main__":
    notes_path = Path("sample_data") / "notes.txt"
    text = read_text_file(str(notes_path))

    print("Study material loaded successfully!")
    print(f"Characters loaded: {len(text)}")
    print("\nPreview:\n")
    print(text[:300])
