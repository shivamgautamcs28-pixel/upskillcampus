"""
main.py
Entry point for the Python Quiz Game.
Ensures the database exists, then launches the GUI.
"""

import os

from db_setup import DB_FILE, initialize_db
from gui import QuizApp


def main():
    if not os.path.exists(DB_FILE):
        initialize_db()
    app = QuizApp()
    app.mainloop()


if __name__ == "__main__":
    main()
