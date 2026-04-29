import json
import os

HISTORY_FILE = "history.json"


def load_history() -> list:
    """
    Загружает историю сгенерированных цитат из файла history.json.

    Returns:
        list: Список записей. Пустой список при отсутствии файла или ошибке.
    """
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_history(history: list) -> None:
    """
    Сохраняет историю цитат в файл history.json.

    Args:
        history: Список записей для сохранения.
    """
    with open(HISTORY_FILE, "w", encoding="utf-8") as fh:
        json.dump(history, fh, ensure_ascii=False, indent=2)
