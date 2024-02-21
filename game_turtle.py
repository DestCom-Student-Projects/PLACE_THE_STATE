import pandas as pd
import turtle
from tkinter import simpledialog, messagebox
import os

state_data = pd.read_csv(os.path.join("assets", "50_states.csv"))

window = turtle.Screen()
window.title("State Quiz")
image_path = os.path.join("assets", "blank_states_img.gif")
window.addshape(image_path)
turtle.shape(image_path)

pen = turtle.Turtle()
pen.penup()
pen.hideturtle()

score = 0
time_remaining = 600

def finish_game():
    global score
    window.bye()
    messagebox.showinfo("K.O", f"Final Score: {score} !")

def verify(guess):
    global score
    if guess in state_data['state'].values:
        state_info = state_data[state_data['state'] == guess]
        x_coord = int(state_info['x'].iloc[0])
        y_coord = int(state_info['y'].iloc[0])
        pen.goto(x_coord, y_coord)
        pen.write(guess, align='center', font=('Arial', 8, 'normal'))
        score += 1
        window.update()

def time_count():
    global time_remaining
    if time_remaining > 0:
        time_remaining -= 1
        window.title(f"State Location Game - Score: {score} - Remaining: {time_remaining}")
        window.ontimer(time_count, 1000)
    elif time_remaining == 0:
        finish_game()


time_count()

while time_remaining > 0:
    guess = simpledialog.askstring("FIND", "Enter the name of a state")
    if guess is None:
        break
    guess = guess.title()
    verify(guess)
