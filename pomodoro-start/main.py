from tkinter import *
from tkinter_unblur import Tk
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 1
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- # 

# ---------------------------- TIMER MECHANISM ------------------------------- # 

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 

def reset_timer():
    window.after_cancel(timer)
    # timer_text 00:00
    canvas.itemconfig(timer_text, text="00:00")
    #timer_label "Timer"
    timer_label['text'] = "Timer"
    # Reset checkmarks
    global reps
    reps = 0

def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN *60

    if reps % 8 == 0: #long break every 8 rounds
        timer_label.config(text="Break", fg=RED)
        count_down(long_break_sec)
    elif reps % 2 == 0: #short break every 2 rounds
        timer_label.config(text="Break", fg=PINK)
        count_down(short_break_sec)
    else:
        timer_label.config(text="Work", fg=GREEN)
        count_down(work_sec) #work every other rounds




def count_down(count):

    count_min = math.floor(count / 60)
    count_sec = count % 60

    # % operator basically returns the decimal part of the division
    # and then multiplies by the number you divided by
    # 7%3 returns the decimal part of 7/3 and multiplies it by 3
    # 7/3 = 2.3333333, and 7%3 basically returns 0.333333*3 which is 1

    if count_sec < 10:
        count_sec = f"0{count_sec}"


    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count-1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✔"
        checkmark_label.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.call('tk', 'scaling', 2)
window.config(padx=100, pady=50, bg=YELLOW)
window.config(bg=YELLOW)

canvas = Canvas(width=200, height=224 , bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill='white', font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

timer_label = Label(text="Timer", font=(FONT_NAME, 50), fg=GREEN, bg=YELLOW)
timer_label.grid(row=0, column=1)

start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(row=2, column=0)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(row=2, column=2)

checkmark_label = Label(fg=GREEN, bg=YELLOW)
checkmark_label.grid(row=3, column=1)


window.mainloop()