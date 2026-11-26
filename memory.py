import json
from pathlib import Path

MEMORY_FILE = Path("chat_history.json")


def load_memory():
    if not MEMORY_FILE.exists():
        return []

    try:
        with MEMORY_FILE.open("r", encoding="utf-8") as file:
            history = json.load(file)

        if isinstance(history, list):
            return history

        return []

    except (json.JSONDecodeError, OSError):
        return []


def save_memory(history):
    with MEMORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)


def clear_memory():
    save_memory([])