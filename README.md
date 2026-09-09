# Python Quiz Game

A desktop quiz application built in Python. It reads questions from a SQLite
database, presents them through a Tkinter interface, and tracks the user's
score in real time across multiple topics.

## Features
- Questions stored in a SQLite database (`quiz.db`)
- Four topic categories: General Knowledge, Science, History, Geography
- Supports multiple-choice and True/False questions
- Weighted scoring (10 pts for MCQ, 5 pts for True/False)
- Simple Tkinter GUI with progress tracking and a results screen
- Unit tests covering the scoring engine

## Project Structure
```
quiz_game/
├── main.py              # Entry point
├── db_setup.py           # Creates and seeds the SQLite database
├── quiz_engine.py         # Core quiz logic (loading, scoring, validation)
├── gui.py                 # Tkinter user interface
├── tests/
│   └── test_quiz_engine.py
├── requirements.txt
└── README.md
```

## Requirements
- Python 3.8+
- No external dependencies (uses only `sqlite3` and `tkinter`, both in the
  Python standard library)

## Setup & Run
```bash
# 1. Clone the repository
git clone <your-repo-url>
cd quiz_game

# 2. (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Run the app (creates quiz.db automatically on first run)
python main.py
```

## Running Tests
```bash
python -m unittest discover -s tests
```

## Rebuilding the Question Bank
To reset and reseed the database:
```bash
python db_setup.py
```

## Future Enhancements
- Timed questions
- Difficulty levels
- Leaderboard / high-score tracking
- Export results to a report file
