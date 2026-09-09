"""
test_quiz_engine.py
Unit tests for QuizEngine covering loading, scoring, and completion behavior.
Run with: python -m unittest discover
"""

import os
import sqlite3
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from quiz_engine import QuizEngine  # noqa: E402

TEST_DB = "test_quiz.db"


class TestQuizEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        conn = sqlite3.connect(TEST_DB)
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE questions (
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
            """
        )
        cur.executemany(
            """INSERT INTO questions
               (category, question, option_a, option_b, option_c, option_d, correct_option, qtype)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                ("Science", "Water boils at 100C at sea level.", "True", "False", None, None, "A", "tf"),
                ("General Knowledge", "Capital of France?", "Paris", "Rome", "Berlin", "Madrid", "A", "mcq"),
            ],
        )
        conn.commit()
        conn.close()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_loads_questions(self):
        engine = QuizEngine(db_path=TEST_DB, num_questions=2)
        self.assertEqual(engine.get_total_questions(), 2)

    def test_correct_answer_increases_score(self):
        engine = QuizEngine(db_path=TEST_DB, num_questions=2)
        question = engine.get_current_question()
        result = engine.submit_answer(question["correct"])
        self.assertTrue(result)
        self.assertGreater(engine.get_score(), 0)

    def test_incorrect_answer_does_not_increase_score(self):
        engine = QuizEngine(db_path=TEST_DB, num_questions=2)
        question = engine.get_current_question()
        wrong_option = "B" if question["correct"] != "B" else "A"
        result = engine.submit_answer(wrong_option)
        self.assertFalse(result)
        self.assertEqual(engine.get_score(), 0)

    def test_quiz_ends_after_all_questions(self):
        engine = QuizEngine(db_path=TEST_DB, num_questions=2)
        engine.submit_answer(engine.get_current_question()["correct"])
        engine.submit_answer(engine.get_current_question()["correct"])
        self.assertFalse(engine.has_next())
        self.assertIsNone(engine.get_current_question())


if __name__ == "__main__":
    unittest.main()
