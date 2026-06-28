from tkinter import *
from tkinter_unblur import Tk
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"

class QuizInterface:
    def __init__(self, quiz: QuizBrain):
        self.quiz = quiz
        self.window = Tk()
        self.window.title('Quizzler')
        self.window.config(padx=20, pady=20, background=THEME_COLOR)
        self.window.call('tk', 'scaling', 2)

        self.score_label = Label(text='Score: 0', bg=THEME_COLOR, fg='white')
        self.score_label.grid(row=0, column=1)

        self.canvas = Canvas(width=600, height=500)
        self.question_text = self.canvas.create_text(
            300,
            250,
            text='Some Question Text',
            width=580,
            font=('Arial', 20, 'italic'),
            fill=THEME_COLOR
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        true_image = PhotoImage(file='images/true.png')
        self.true_button = Button(image=true_image, highlightthickness=0, command=self.true_pressed)
        self.true_button.grid(row=2,column=0)

        false_image = PhotoImage(file='images/false.png')
        self.false_button = Button(image=false_image, highlightthickness=0, command=self.false_pressed)
        self.false_button.grid(row=2,column=1)

        self.get_next_question()


        self.window.mainloop()

    def get_next_question(self):
        if not self.quiz.still_has_questions():
            self.canvas.itemconfig(self.question_text, text="You've reached the end of the quiz.")
            return

        self.canvas.config(bg='white')
        self.score_label.config(text=f"Score: {self.quiz.score}")
        q_text = self.quiz.next_question()
        self.canvas.itemconfig(self.question_text, text=q_text)

    def true_pressed(self):
        self.give_feedback(self.quiz.check_answer('true'))

    def false_pressed(self):
        is_right = self.quiz.check_answer('false')
        self.give_feedback(is_right)

    def give_feedback(self, is_right):
        if not self.quiz.still_has_questions():
            self.canvas.itemconfig(self.question_text, text="You've reached the end of the quiz.")
            return

        if is_right:
            self.canvas.config(bg='green')
        else:
            self.canvas.config(bg='red')

        self.window.after(1000, self.get_next_question)
