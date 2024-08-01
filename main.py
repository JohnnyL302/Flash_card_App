import time
from tkinter import *
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"
current_card = {}

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(top_text, text="French", fill="black")
    canvas.itemconfig(bottom_text, text=current_card["French"], fill="black")
    canvas.itemconfig(card, image=card_front)
    flip_timer = window.after(3000, func=flip_card)
def flip_card():
    canvas.itemconfig(card, image=card_back)
    canvas.itemconfig(top_text, text="English",fill="white")
    canvas.itemconfig(bottom_text, text=current_card["English"], fill="white")

def is_known():
    to_learn.remove(current_card)
    new_data = pandas.DataFrame(to_learn)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


try:
    pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
    to_learn = data.to_dict(orient="records")
else:
    data = pandas.read_csv("data/words_to_learn.csv")
    to_learn = data.to_dict(orient="records")


# -------------------------UI SETUP--------------------------------------------- #
window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card = canvas.create_image(400, 263, image=card_front)
top_text = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
bottom_text = canvas.create_text(400,253, text="Word", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)


check_image = PhotoImage(file="images/right.png")
check_button = Button(image=check_image, highlightthickness= 0, command=is_known)
check_button.grid(row=1, column=1)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

next_card()

window.mainloop()


