import random
from tkinter import *
from tkinter_unblur import Tk
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}


# Fixed: Handled FileNotFoundError for first-time users
# and EmptyDataError if words_to_learn.csv is empty to prevent crashes.
try:
    data = pandas.read_csv('data/words_to_learn.csv')
except (FileNotFoundError, pandas.errors.EmptyDataError):
    original_data = pandas.read_csv('data/french_words.csv')
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn = data.to_dict(orient='records')

try:
    data = pandas.read_csv('data/words_to_learn.csv')
except (FileNotFoundError, pandas.errors.EmptyDataError):
    original_data = pandas.read_csv('data/french_words.csv')
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn = data.to_dict(orient='records')

def generate_new_flashcard():
    global current_card, flip_timer
    try:
        window.after_cancel(flip_timer)
    except NameError:
        pass
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_word, text=current_card['French'], fill='black')
    canvas.itemconfig(card_title, text='French', fill='black')
    canvas.itemconfig(canvas_image, image=card_front_image)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(canvas_image, image=card_back_image)
    canvas.itemconfig(card_word, text=current_card['English'], fill='white')
    canvas.itemconfig(card_title, text='English', fill='white')

def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv('data/words_to_learn.csv', index=False)

    generate_new_flashcard()

window = Tk()
window.title("Flashy")
window.config(background=BACKGROUND_COLOR, padx=50, pady=50)
window.call('tk', 'scaling', 2)

# Canvas
card_front_image = PhotoImage(file='images/card_front.png')
card_back_image = PhotoImage(file='images/card_back.png')
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas.create_image(400, 263, image=card_front_image)
canvas.grid(row=0, column=0, columnspan=2)
card_title = canvas.create_text(400, 150, text='French', font=('Ariel', 40, 'italic'))
card_word = canvas.create_text(400, 263, text='word', font=('Ariel', 60, 'bold'))

# Buttons
wrong_button_img = PhotoImage(file='images/wrong.png')
wrong_button = Button(image=wrong_button_img, bd=0, bg=BACKGROUND_COLOR, command=generate_new_flashcard)
wrong_button.grid(row=1, column=0)

right_button_img = PhotoImage(file='images/right.png')
right_button = Button(image=right_button_img, bd=0, bg=BACKGROUND_COLOR, command=is_known)
right_button.grid(row=1, column=1)


generate_new_flashcard()


window.mainloop()
