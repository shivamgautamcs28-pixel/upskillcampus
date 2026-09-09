"""
db_setup.py
Creates the SQLite database and seeds it with quiz questions.
Run directly (python db_setup.py) to (re)build the database.
"""

import sqlite3

DB_FILE = "quiz.db"

QUESTIONS = [
    # category, question, option_a, option_b, option_c, option_d, correct_option, qtype
    ("General Knowledge", "What is the capital of France?", "Paris", "Rome", "Berlin", "Madrid", "A", "mcq"),
    ("General Knowledge", "Which language has the most native speakers?", "English", "Mandarin Chinese", "Spanish", "Hindi", "B", "mcq"),
    ("General Knowledge", "The Great Wall of China is visible from space with the naked eye.", "True", "False", None, None, "B", "tf"),
    ("General Knowledge", "How many continents are there on Earth?", "5", "6", "7", "8", "C", "mcq"),
    ("General Knowledge", "Honey never spoils.", "True", "False", None, None, "A", "tf"),
    ("General Knowledge", "Which currency is used in Japan?", "Won", "Yuan", "Yen", "Ringgit", "C", "mcq"),

    ("Science", "What is the chemical symbol for gold?", "Ag", "Au", "Gd", "Go", "B", "mcq"),
    ("Science", "Water boils at 100°C at sea level.", "True", "False", None, None, "A", "tf"),
    ("Science", "What planet is known as the Red Planet?", "Venus", "Mars", "Jupiter", "Saturn", "B", "mcq"),
    ("Science", "Humans have 46 chromosomes.", "True", "False", None, None, "A", "tf"),
    ("Science", "What is the powerhouse of the cell?", "Nucleus", "Ribosome", "Mitochondria", "Golgi body", "C", "mcq"),
    ("Science", "Which gas do plants primarily absorb for photosynthesis?", "Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen", "C", "mcq"),

    ("History", "Who was the first President of the United States?", "Thomas Jefferson", "George Washington", "John Adams", "Abraham Lincoln", "B", "mcq"),
    ("History", "World War II ended in 1945.", "True", "False", None, None, "A", "tf"),
    ("History", "The Great Depression began in which year?", "1919", "1929", "1939", "1949", "B", "mcq"),
    ("History", "The Roman Empire fell before the Egyptian pyramids were built.", "True", "False", None, None, "B", "tf"),
    ("History", "Who wrote the Declaration of Independence?", "Benjamin Franklin", "Thomas Jefferson", "John Hancock", "James Madison", "B", "mcq"),
    ("History", "The Berlin Wall fell in which year?", "1979", "1989", "1999", "1969", "B", "mcq"),

    ("Geography", "What is the longest river in the world?", "Amazon", "Nile", "Yangtze", "Mississippi", "B", "mcq"),
    ("Geography", "Mount Everest is located in Nepal.", "True", "False", None, None, "A", "tf"),
    ("Geography", "Which is the smallest country in the world?", "Monaco", "San Marino", "Vatican City", "Liechtenstein", "C", "mcq"),
    ("Geography", "Australia is both a country and a continent.", "True", "False", None, None, "A", "tf"),
    ("Geography", "Which desert is the largest in the world?", "Sahara", "Gobi", "Antarctic", "Arabian", "C", "mcq"),
    ("Geography", "How many countries border Germany?", "6", "7", "9", "11", "C", "mcq"),
]


def initialize_db(db_file: str = DB_FILE, force: bool = False) -> None:
    """Create the questions table and seed it if it's empty (or if force=True)."""
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT,
            option_d TEXT,
            correct_option TEXT NOT NULL,
            qtype TEXT NOT NULL DEFAULT 'mcq'
        )
    """)

    if force:
        cur.execute("DELETE FROM questions")

    cur.execute("SELECT COUNT(*) FROM questions")
    count = cur.fetchone()[0]

    if count == 0:
        cur.executemany(
            """INSERT INTO questions
               (category, question, option_a, option_b, option_c, option_d, correct_option, qtype)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            QUESTIONS,
        )
        conn.commit()
        print(f"Seeded database with {len(QUESTIONS)} questions.")
    else:
        print(f"Database already contains {count} questions. Skipping seed.")

    conn.close()


if __name__ == "__main__":
    initialize_db(force=True)
