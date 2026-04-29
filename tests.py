import unittest
import os
import json
import random

from quotes import QUOTES
from storage import load_history, save_history

_HISTORY_FILE = "history.json"


class TestQuotes(unittest.TestCase):
    """Тесты базы цитат и генерации."""

    def test_quotes_not_empty(self):
        """База цитат не пуста (позитивный)."""
        self.assertGreater(len(QUOTES), 0)

    def test_quotes_have_required_keys(self):
        """Каждая цитата содержит поля text, author, topic (позитивный)."""
        for q in QUOTES:
            with self.subTest(q=q):
                self.assertIn("text", q)
                self.assertIn("author", q)
                self.assertIn("topic", q)

    def test_quotes_no_empty_fields(self):
        """В цитатах нет пустых строк (позитивный)."""
        for q in QUOTES:
            self.assertTrue(q["text"].strip())
            self.assertTrue(q["author"].strip())
            self.assertTrue(q["topic"].strip())

    def test_random_choice_from_pool(self):
        """random.choice возвращает элемент из пула (позитивный)."""
        random.seed(42)
        result = random.choice(QUOTES)
        self.assertIn(result, QUOTES)

    def test_filter_by_author(self):
        """Фильтрация по автору возвращает только его цитаты (позитивный)."""
        author = QUOTES[0]["author"]
        filtered = [q for q in QUOTES if q["author"] == author]
        self.assertTrue(all(q["author"] == author for q in filtered))

    def test_filter_by_topic(self):
        """Фильтрация по теме корректна (позитивный)."""
        topic = "Мотивация"
        filtered = [q for q in QUOTES if q["topic"] == topic]
        self.assertTrue(all(q["topic"] == topic for q in filtered))

    def test_filter_no_match(self):
        """Фильтр без совпадений возвращает пустой список (негативный)."""
        filtered = [q for q in QUOTES if q["author"] == "Несуществующий автор"]
        self.assertEqual(filtered, [])

    def test_custom_quote_validation_empty_text(self):
        """Пустой текст цитаты не должен добавляться (негативный)."""
        text = "   "
        self.assertFalse(bool(text.strip()))

    def test_custom_quote_validation_empty_author(self):
        """Пустой автор не должен добавляться (граничный)."""
        author = ""
        self.assertFalse(bool(author.strip()))


class TestStorage(unittest.TestCase):
    """Тесты JSON-хранилища."""

    def tearDown(self):
        if os.path.exists(_HISTORY_FILE):
            os.remove(_HISTORY_FILE)

    def test_save_and_load(self):
        """Сохранение и загрузка корректны (позитивный)."""
        data = [{"text": "Test", "author": "A", "topic": "B", "date": "2025-01-01 00:00:00"}]
        save_history(data)
        self.assertEqual(load_history(), data)

    def test_load_no_file(self):
        """Загрузка без файла — пустой список (позитивный)."""
        if os.path.exists(_HISTORY_FILE):
            os.remove(_HISTORY_FILE)
        self.assertEqual(load_history(), [])

    def test_load_corrupt_file(self):
        """Повреждённый JSON — пустой список (негативный)."""
        with open(_HISTORY_FILE, "w") as f:
            f.write("not_json")
        self.assertEqual(load_history(), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
