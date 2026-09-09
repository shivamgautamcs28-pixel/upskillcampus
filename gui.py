"""
gui.py
Tkinter-based user interface for the quiz game.
"""

import tkinter as tk
from tkinter import messagebox

from quiz_engine import QuizEngine


class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Quiz Game")
        self.geometry("500x420")
        self.resizable(False, False)

        self.engine = None
        self.selected_option = tk.StringVar()

        self._build_start_screen()

    def _clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def _build_start_screen(self):
        self._clear_screen()
        tk.Label(self, text="Python Quiz Game", font=("Arial", 20, "bold")).pack(pady=40)
        tk.Label(
            self, text="Test your knowledge across multiple topics!", font=("Arial", 12)
        ).pack(pady=10)
        tk.Button(
            self, text="Start Quiz", font=("Arial", 14), width=15, command=self._start_quiz
        ).pack(pady=30)

    def _start_quiz(self):
        self.engine = QuizEngine(num_questions=10)
        self._show_question()

    def _show_question(self):
        self._clear_screen()
        question = self.engine.get_current_question()
        if question is None:
            self._show_results()
            return

        progress = f"Question {self.engine.current_index + 1} of {self.engine.get_total_questions()}"
        tk.Label(self, text=progress, font=("Arial", 10)).pack(pady=(15, 0))
        tk.Label(self, text=f"[{question['category']}]", font=("Arial", 10, "italic")).pack()
        tk.Label(
            self,
            text=question["text"],
            font=("Arial", 14, "bold"),
            wraplength=440,
            justify="left",
        ).pack(pady=20)

        self.selected_option.set("")
        for key, text in question["options"].items():
            tk.Radiobutton(
                self,
                text=f"{key}. {text}",
                variable=self.selected_option,
                value=key,
                font=("Arial", 12),
                anchor="w",
            ).pack(fill="x", padx=60, pady=2)

        tk.Button(
            self, text="Submit Answer", font=("Arial", 12), command=self._submit_answer
        ).pack(pady=25)

    def _submit_answer(self):
        if not self.selected_option.get():
            messagebox.showwarning(
                "No answer selected", "Please select an answer before continuing."
            )
            return
        self.engine.submit_answer(self.selected_option.get())
        self._show_question()

    def _show_results(self):
        self._clear_screen()
        score = self.engine.get_score()
        max_score = self.engine.get_max_score()
        total = self.engine.get_total_questions()
        correct = sum(1 for a in self.engine.answers_log if a["is_correct"])

        tk.Label(self, text="Quiz Complete!", font=("Arial", 20, "bold")).pack(pady=30)
        tk.Label(
            self, text=f"You got {correct} out of {total} correct.", font=("Arial", 14)
        ).pack(pady=10)
        tk.Label(
            self, text=f"Final Score: {score} / {max_score}", font=("Arial", 16, "bold")
        ).pack(pady=10)
        tk.Button(
            self, text="Play Again", font=("Arial", 12), width=15, command=self._build_start_screen
        ).pack(pady=15)
        tk.Button(self, text="Quit", font=("Arial", 12), width=15, command=self.destroy).pack()


if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
