import sqlite3
from typing import List, Dict, Any

class DatabaseManager:
    """
    Класс для управления базой данных SQLite для хранения результатов транскрибации.
    """
    def __init__(self, db_path: str):
        """
        Инициализирует менеджер базы данных и создает таблицу, если она не существует.

        Args:
            db_path (str): Путь к файлу базы данных SQLite.
        """
        self.db_path = db_path
        self.conn = None
        try:
            # timeout предотвращает dead-lock при параллельном доступе
            self.conn = sqlite3.connect(db_path, timeout=10)
            self._create_table()
        except sqlite3.Error as e:
            print(f"Ошибка подключения к базе данных: {e}")
            raise

    def _create_table(self):
        """
        Создает таблицу 'words' для хранения слов и их временных меток,
        если она еще не существует.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT NOT NULL,
                    start_time REAL NOT NULL,
                    end_time REAL NOT NULL
                )
            """)
            # если старая версия таблицы уже существует без end_time, добавляем столбец
            cursor.execute("PRAGMA table_info(words)")
            cols = [row[1] for row in cursor.fetchall()]
            if 'end_time' not in cols:
                cursor.execute("ALTER TABLE words ADD COLUMN end_time REAL NOT NULL DEFAULT 0")
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при создании таблицы: {e}")

    def save_words(self, words_data: List[Dict[str, Any]]):
        """
        Сохраняет список распознанных слов в базу данных.

        Args:
            words_data (List[Dict[str, Any]]): Список словарей,
            где каждый словарь содержит 'word' и 'start'.
        """
        if not self.conn:
            print("Нет подключения к базе данных. Сохранение невозможно.")
            return

        try:
            cursor = self.conn.cursor()
            # Перед вставкой новых данных очищаем старые
            cursor.execute("DELETE FROM words")
            
            words_to_insert = [(item['word'], item['start'], item['end']) for item in words_data]
            
            cursor.executemany("INSERT INTO words (word, start_time, end_time) VALUES (?, ?, ?)", words_to_insert)
            
            self.conn.commit()
            print(f"Успешно сохранено {len(words_to_insert)} слов в базу данных.")
        except sqlite3.Error as e:
            print(f"Ошибка при сохранении слов в базу данных: {e}")
            self.conn.rollback() # Откатываем изменения в случае ошибки

    def __del__(self):
        """
        Закрывает соединение с базой данных при уничтожении объекта.
        """
        if self.conn:
            self.conn.close()
