import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import datetime

from quotes import QUOTES
from storage import load_history, save_history


def get_unique_values(key: str, source: list) -> list:
    """Возвращает отсортированный список уникальных значений по ключу."""
    return sorted(set(q[key] for q in source))


def on_generate():
    """Выбирает случайную цитату и добавляет её в историю."""
    pool = get_filtered_pool()
    if not pool:
        messagebox.showinfo("Нет цитат", "По выбранному фильтру цитаты не найдены.")
        return

    quote = random.choice(pool)
    display_quote(quote)

    record = {
        "text": quote["text"],
        "author": quote["author"],
        "topic": quote["topic"],
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    history.append(record)
    save_history(history)
    refresh_history_list()


def get_filtered_pool() -> list:
    """Возвращает список цитат, соответствующих выбранным фильтрам."""
    author_filter = filter_author_combo.get()
    topic_filter = filter_topic_combo.get()

    pool = all_quotes[:]
    if author_filter and author_filter != "Все":
        pool = [q for q in pool if q["author"] == author_filter]
    if topic_filter and topic_filter != "Все":
        pool = [q for q in pool if q["topic"] == topic_filter]
    return pool


def display_quote(quote: dict):
    """Отображает выбранную цитату в текстовом поле."""
    quote_text.config(state=tk.NORMAL)
    quote_text.delete("1.0", tk.END)
    quote_text.insert(tk.END, f'"{quote["text"]}"\n\n— {quote["author"]}  |  Тема: {quote["topic"]}')
    quote_text.config(state=tk.DISABLED)


def refresh_history_list():
    """Обновляет список истории цитат."""
    history_listbox.delete(0, tk.END)
    for rec in history:
        history_listbox.insert(
            tk.END,
            f'[{rec.get("date", "")}]  {rec["author"]}: «{rec["text"][:60]}…»'
            if len(rec["text"]) > 60
            else f'[{rec.get("date", "")}]  {rec["author"]}: «{rec["text"]}»'
        )


def on_add_custom():
    """Открывает диалог для добавления пользовательской цитаты."""
    text = simpledialog.askstring("Новая цитата", "Введите текст цитаты:")
    if text is None:
        return
    if not text.strip():
        messagebox.showerror("Ошибка", "Текст цитаты не может быть пустым.")
        return
    author = simpledialog.askstring("Новая цитата", "Введите автора:")
    if author is None:
        return
    if not author.strip():
        messagebox.showerror("Ошибка", "Имя автора не может быть пустым.")
        return
    topic = simpledialog.askstring("Новая цитата", "Введите тему:")
    if topic is None:
        return
    if not topic.strip():
        messagebox.showerror("Ошибка", "Тема не может быть пустой.")
        return

    all_quotes.append({"text": text.strip(), "author": author.strip(), "topic": topic.strip()})
    update_filter_combos()
    messagebox.showinfo("Успех", "Цитата добавлена!")


def update_filter_combos():
    """Обновляет значения выпадающих списков фильтра."""
    authors = ["Все"] + get_unique_values("author", all_quotes)
    topics = ["Все"] + get_unique_values("topic", all_quotes)
    filter_author_combo["values"] = authors
    filter_topic_combo["values"] = topics


# ── Главное окно ──────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Random Quote Generator — Генератор цитат")
root.geometry("750x620")
root.resizable(False, False)

all_quotes = QUOTES[:]

# ── Фильтры ───────────────────────────────────────────────────────────────────
flt = tk.LabelFrame(root, text="Фильтр генерации", padx=10, pady=6)
flt.pack(fill=tk.X, padx=12, pady=8)

tk.Label(flt, text="Автор:").grid(row=0, column=0, sticky=tk.W)
filter_author_combo = ttk.Combobox(flt, state="readonly", width=22)
filter_author_combo.grid(row=0, column=1, padx=6)

tk.Label(flt, text="Тема:").grid(row=0, column=2, sticky=tk.W, padx=(16, 0))
filter_topic_combo = ttk.Combobox(flt, state="readonly", width=18)
filter_topic_combo.grid(row=0, column=3, padx=6)

update_filter_combos()
filter_author_combo.set("Все")
filter_topic_combo.set("Все")

# ── Кнопки ────────────────────────────────────────────────────────────────────
btn_frm = tk.Frame(root)
btn_frm.pack(fill=tk.X, padx=12)
tk.Button(
    btn_frm, text="🎲  Сгенерировать цитату", command=on_generate,
    bg="#9C27B0", fg="white", padx=14, pady=5,
).pack(side=tk.LEFT, padx=4)
tk.Button(
    btn_frm, text="➕  Добавить свою цитату", command=on_add_custom,
    bg="#FF9800", fg="white", padx=14, pady=5,
).pack(side=tk.LEFT, padx=4)

# ── Отображение цитаты ────────────────────────────────────────────────────────
quote_frm = tk.LabelFrame(root, text="Цитата", padx=8, pady=6)
quote_frm.pack(fill=tk.X, padx=12, pady=8)
quote_text = tk.Text(quote_frm, height=4, wrap=tk.WORD, font=("Georgia", 11), state=tk.DISABLED)
quote_text.pack(fill=tk.X)

# ── История ───────────────────────────────────────────────────────────────────
hist_frm = tk.LabelFrame(root, text="История сгенерированных цитат", padx=8, pady=6)
hist_frm.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)
history_listbox = tk.Listbox(hist_frm, font=("Consolas", 9), height=12)
sb = ttk.Scrollbar(hist_frm, orient=tk.VERTICAL, command=history_listbox.yview)
history_listbox.configure(yscrollcommand=sb.set)
history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
sb.pack(side=tk.RIGHT, fill=tk.Y)

# ── Загрузка истории ──────────────────────────────────────────────────────────
history = load_history()
refresh_history_list()

root.mainloop()
