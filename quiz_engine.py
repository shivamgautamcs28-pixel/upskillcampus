"""
quiz_engine.py
Core quiz logic: loads questions from the database, tracks progress,
validates answers, and calculates the score.
"""

import random
import sqlite3

from db_setup import DB_FILE

MCQ_POINTS = 10
TF_POINTS = 5


class QuizEngine:
    def __init__(self, db_path: str = DB_FILE, num_questions: int = 10):
        self.db_path = db_path
        self.num_questions = num_questions
        self.questions = []
        self.current_index = 0
        self.score = 0
        self.answers_log = []
        self._load_questions()

    def _load_questions(self) -> None:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            """SELECT id, category, question, option_a, option_b,
                      option_c, option_d, correct_option, qtype
               FROM questions"""
        )
        rows = cur.fetchall()
        conn.close()

        random.shuffle(rows)
        selected = rows[: self.num_questions]

        for qid, category, text, a, b, c, d, correct, qtype in selected:
            options = {"A": a, "B": b}
            if c:
                options["C"] = c
            if d:
                options["D"] = d
            self.questions.append(
                {
                    "id": qid,
                    "category": category,
                    "text": text,
                    "options": options,
                    "correct": correct,
                    "qtype": qtype,
                }
            )

    def has_next(self) -> bool:
        return self.current_index < len(self.questions)

    def get_current_question(self):
        if not self.has_next():
            return None
        return self.questions[self.current_index]

    def submit_answer(self, selected_option: str) -> bool:
        question = self.get_current_question()
        if question is None:
            raise ValueError("No active question to answer.")

        is_correct = selected_option.strip().upper() == question["correct"].strip().upper()
        points = TF_POINTS if question["qtype"] == "tf" else MCQ_POINTS

        if is_correct:
            self.score += points

        self.answers_log.append(
            {
                "question_id": question["id"],
                "selected": selected_option,
                "correct": question["correct"],
                "is_correct": is_correct,
                "points": points if is_correct else 0,
            }
        )

        self.current_index += 1
        return is_correct

    def get_score(self) -> int:
        return self.score

    def get_max_score(self) -> int:
        return sum(TF_POINTS if q["qtype"] == "tf" else MCQ_POINTS for q in self.questions)

    def get_total_questions(self) -> int:
        return len(self.questions)
