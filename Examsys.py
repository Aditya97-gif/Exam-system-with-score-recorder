import tkinter as tk
from tkinter import messagebox
import requests
import html

def fetch_questions(amount=5):
    url = f"https://opentdb.com/api.php?amount={amount}&type=multiple"
    response = requests.get(url)
    data = response.json()
    questions = []
    for item in data['results']:
        q = {
            'question': html.unescape(item['question']),
            'options': [html.unescape(opt) for opt in item['incorrect_answers'] + [item['correct_answer']]],
            'answer': html.unescape(item['correct_answer'])
        }
        import random
        random.shuffle(q['options'])
        questions.append(q)
    return questions

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("700x500")  
        self.score = 0
        self.qn = 0
        self.student_id = None
        self.questions = fetch_questions(5)
        self.user_answers = []
        self.ask_student_id()

    def ask_student_id(self):
        self.id_window = tk.Toplevel(self.root)
        self.id_window.title("Enter Student ID")
        self.id_window.geometry("350x150")  
        tk.Label(self.id_window, text="Enter your Student ID:", font=("Arial", 12)).pack(padx=20, pady=10)
        self.id_entry = tk.Entry(self.id_window, font=("Arial", 12))
        self.id_entry.pack(padx=20, pady=5)
        tk.Button(self.id_window, text="Start Quiz", command=self.save_student_id).pack(pady=10)
        self.id_window.grab_set()
        self.root.wait_window(self.id_window)

        self.create_widgets()

    def save_student_id(self):
        sid = self.id_entry.get().strip()
        if not sid:
            messagebox.showwarning("Input Error", "Student ID cannot be empty!")
            return
        self.student_id = sid
        self.id_window.destroy()

    def create_widgets(self):
        self.question_label = tk.Label(self.root, text="", wraplength=650, font=("Arial", 16))
        self.question_label.pack(pady=30)

        self.var = tk.StringVar()
        self.options = []
        for i in range(4):
            rb = tk.Radiobutton(self.root, text="", variable=self.var, value="", font=("Arial", 14))
            rb.pack(anchor='w', padx=60)
            self.options.append(rb)

        self.next_btn = tk.Button(self.root, text="Next", font=("Arial", 14), command=self.next_question)
        self.next_btn.pack(pady=30)

        self.show_question()

    def show_question(self):
        q = self.questions[self.qn]
        self.question_label.config(text=f"Q{self.qn+1}: {q['question']}")
        self.var.set(None)
        for i, opt in enumerate(q['options']):
            self.options[i].config(text=opt, value=opt)

    def next_question(self):
        selected = self.var.get()
        if not selected:
            messagebox.showwarning("No selection", "Please select an option!")
            return
        if selected == self.questions[self.qn]['answer']:
            self.score += 1
        self.qn += 1
        if self.qn < len(self.questions):
            self.show_question()
        else:
            self.save_score()
            messagebox.showinfo("Quiz Finished", f"Your Score: {self.score}/{len(self.questions)}\nSaved for Student ID: {self.student_id}")
            self.root.destroy()

    def save_score(self):
        with open("quiz_scores.txt", "a") as f:
            f.write(f"Student ID: {self.student_id}, Score: {self.score}/{len(self.questions)}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()