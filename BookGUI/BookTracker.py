import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.books = []
        self.load_books()

        # --- Создание виджетов ---
        self.create_widgets()
        self.update_treeview()

    def create_widgets(self):
        # Поля ввода
        ttk.Label(self.root, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_entry = ttk.Entry(self.root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Автор:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.author_entry = ttk.Entry(self.root, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Жанр:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.genre_entry = ttk.Entry(self.root, width=30)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Страниц:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.pages_entry = ttk.Entry(self.root, width=30)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        ttk.Button(self.root, text="Добавить книгу", command=self.add_book).grid(row=4, columnspan=2, pady=10)

        # Фильтрация
        ttk.Label(self.root, text="Фильтр по жанру:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.filter_genre = ttk.Entry(self.root, width=30)
        self.filter_genre.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Фильтр по страницам (>):").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.filter_pages = ttk.Entry(self.root, width=30)
        self.filter_pages.grid(row=6, column=1, padx=5, pady=5)

        ttk.Button(self.root, text="Применить фильтр", command=self.apply_filter).grid(row=7, columnspan=2)

        # Таблица (Treeview)
        self.tree = ttk.Treeview(self.root, columns=(1, 2, 3), show='headings', height=12)
        self.tree.grid(row=8, columnspan=2)
        self.tree.heading(1, text="Название")
        self.tree.heading(2, text="Автор")
        self.tree.heading(3, text="Жанр")

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()

        if not title or not author or not genre or not pages:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        if not pages.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return

        self.books.append({
            "title": title,
            "author": author,
            "genre": genre,
            "pages": int(pages)
        })

        self.save_books()
        self.update_treeview()

    def update_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for book in self.books:
            self.tree.insert("", "end", values=(book["title"], book["author"], book["genre"]))

    def apply_filter(self):
        genre_filter = self.filter_genre.get().strip().lower()
        try:
            pages_filter = int(self.filter_pages.get().strip())
            if pages_filter < 0:
                raise ValueError
        except ValueError:
            pages_filter = None

        filtered_books = self.books.copy()

        if genre_filter:
            filtered_books = [b for b in filtered_books if genre_filter in b["genre"].lower()]

        if pages_filter is not None:
            filtered_books = [b for b in filtered_books if b["pages"] > pages_filter]

        for i in self.tree.get_children():
            self.tree.delete(i)

        for book in filtered_books:
            self.tree.insert("", "end", values=(book["title"], book["author"], book["genre"]))

    def save_books(self):
        with open("books.json", "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False)

    def load_books(self):
        if os.path.exists("books.json"):
            with open("books.json", "r", encoding="utf-8") as f:
                self.books = json.load(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()
