from tkinter import *
from tkinter import messagebox
from random import choice
import pandas


# ----------------------------------- CONSTANTS -----------------------------------


BG = "lightcyan1"
ACCENT_BG = "azure1"
FONT = "Times New Roman"


# -------------------------------------- DATA -------------------------------------


try:
    data = pandas.read_csv("verses_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("bible_verses.csv")
finally:
    all_verses_data = pandas.read_csv("bible_verses.csv")
    verses_to_learn = data.to_dict(orient="records")
    current_verse_info = {}
    total_verses_count = len(all_verses_data)


# ----------------------------------- GIVE HINT -----------------------------------


def give_hint():
    global current_verse_info
    verse_text = current_verse_info["Text"]
    verse_hint = verse_text.split()[0:3]
    guess_box.delete("1.0", END)
    guess_box.insert(END, verse_hint)


# --------------------------------- CHECK PRACTICE ----------------------------------


def check_practice():
    global current_verse_info
    verse_text = current_verse_info["Text"].lower().strip()
    verse_guess = guess_box.get("1.0", END).lower().strip()
    if verse_text != verse_guess:
        practice_entry = practice_box.get("1.0", END).lower().strip()
        if practice_entry != verse_text:
            messagebox.showerror(title="Error", message="Write the correct answer exactly as shown above.")
        else:
            new_question()
    else:
        new_question()


# ---------------------------------- NEW QUESTION ----------------------------------


def new_question():
    global current_verse_info
    current_verse_info = choice(verses_to_learn)
    try:
        reset()
    except NameError:
        pass


# ------------------------------------- RESET --------------------------------------


# [{'Reference': 'Genesis 1:1', 'Text': 'In the beginning, God created the Heavens and the earth.'}
def reset():
    global current_verse_info, total_verses_count, data
    reference = current_verse_info["Reference"]
    given_info.config(text=reference, font=(FONT, 30, "italic"), fg="black")
    guess_box.delete("1.0", END)
    guess_box.focus()
    guess_box.grid(column=1, row=1, columnspan=2, rowspan=3)
    hint_button.grid(column=1, row=5, pady=25)
    check_answer_button.grid(column=2, row=5, pady=25)
    known_verses.config(text=f"{total_verses_count - len(data)}/{total_verses_count} correct")
    known_verses.grid(column=1, row=4, columnspan=2)
    correct_verse_text.grid_forget()
    wrong_verse_text.grid_forget()
    wrong_guess_text.grid_forget()
    next_button.grid_forget()
    override_button.grid_forget()
    practice_box.grid_forget()


# --------------------------------- CORRECT ANSWER --------------------------------


def correct_answer():
    global current_verse_info
    given_info.config(text="Correct!", font=(FONT, 50, "italic"), fg="green")
    correct_verse_text.config(text=f"'{current_verse_info["Text"]}'\n\n- {current_verse_info["Reference"]}")
    correct_verse_text.grid(column=1, row=1, columnspan=2, rowspan=3, pady=25)
    next_button.grid(column=1, row=4, columnspan=2, pady=25)
    remove_from_verses()


# ---------------------------------- WRONG ANSWER ---------------------------------


def wrong_answer():
    global current_verse_info
    wrong_guess = guess_box.get("1.0", END)
    given_info.config(text="Incorrect.", font=(FONT, 40, "italic"), fg="red")
    wrong_verse_text.config(text=f"Correct answer: {current_verse_info["Text"]}")
    wrong_verse_text.grid(column=1, row=1, columnspan=2)
    wrong_guess_text.config(text=f"Your answer: {wrong_guess}")
    wrong_guess_text.grid(column=1, row=2, columnspan=2)
    practice_box.grid(column=1, row=3, columnspan=2, pady=25)
    practice_box.delete("1.0", END)
    practice_box.focus()
    practice_box.insert(END, "Copy the correct answer here to practice.")
    override_button.grid(column=1, row=4)
    next_button.grid(column=2, row=4)


# --------------------------------- CHECK ANSWER ----------------------------------


def check_answer():
    global current_verse_info
    verse_text = current_verse_info["Text"].lower().strip()
    verse_guess = guess_box.get("1.0", END).lower().strip()
    guess_box.grid_forget()
    hint_button.grid_forget()
    check_answer_button.grid_forget()
    known_verses.grid_forget()
    if verse_guess == verse_text:
        correct_answer()
    else:
        wrong_answer()


# ------------------------------- REMOVE FROM VERSES -------------------------------


def remove_from_verses():
    global current_verse_info, data, verses_to_learn
    verse_text = current_verse_info["Text"].lower().strip()
    verse_guess = guess_box.get("1.0", END).lower().strip()
    verses_to_learn.remove(current_verse_info)
    if len(verses_to_learn) > 0:
        new_data = pandas.DataFrame(verses_to_learn)
        new_data.to_csv("verses_to_learn.csv", index=False)
        data = pandas.read_csv("verses_to_learn.csv")
        if verse_text != verse_guess:
            new_question()
    else:
        data = pandas.read_csv("bible_verses.csv")
        verses_to_learn = data.to_dict(orient="records")
        messagebox.showinfo(title="Complete!", message="Congrats! You've learned everything!\nClick OK to start over.")
        new_question()


# -------------------------------------- UI ---------------------------------------


# window
window = Tk()
window.title("Study")
window.config(padx=100, pady=50, bg=BG)
new_question()


# inputs
guess_box = Text(height=6, width=50, bg=ACCENT_BG)
practice_box = Text(height = 4, width=50, bg=ACCENT_BG)


# labels
given_info = Label(text="", bg=BG)
given_info.grid(column=1, row=0, columnspan=2, pady=25)

known_verses = Label(text=f"{total_verses_count - len(data)}/{total_verses_count} verses learned", font=(FONT, 12, "italic"), bg=BG, fg="grey")

correct_verse_text = Label(text=f"'{current_verse_info["Text"]}'\n\n- {current_verse_info["Reference"]}",
                           font=(FONT, 15),
                           bg=BG,
                           wraplength=400)

wrong_verse_text = Label(text=f"Correct answer: {current_verse_info["Text"]}",
                         font=(FONT, 12),
                         bg=BG,
                         fg="green",
                         wraplength=400,
                         justify="left")

wrong_guess_text = Label(text="",
                         font=(FONT, 12),
                         bg=BG,
                         fg="red",
                         wraplength=400,
                         justify="left")


# buttons
hint_button = Button(text="Hint", font=(FONT, 15), width=12, bg=ACCENT_BG, command=give_hint)
check_answer_button = Button(text="Check Answer", font=(FONT, 15), width=12, bg=ACCENT_BG, command=check_answer)
next_button = Button(text="Next", font=(FONT, 15), width=12, bg=ACCENT_BG, command=check_practice)
override_button = Button(text="Override", font=(FONT, 15), width=12, bg=ACCENT_BG, command=remove_from_verses)


# initial setup
reset()
window.mainloop()

