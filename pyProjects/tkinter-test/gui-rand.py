import Tkinter as tk
import random # for random functions

window = tk.Tk()

diceMax = 2

def RandomNumber():
    MyRandom = random.randint(1, diceMax)
    dice_thrown.configure(text="Dice thrown: " + str(MyRandom))

def closeApp():
    window.destroy()

# CLOSE APP
# --------------
def key(event):
    # '\x17' is the escape sequence for ctrl+w (close in windows apps)
    if(event.char == '\x17'):
        closeApp()

window.title("TestApp")
window.geometry("400x400")

# detect key input
window.bind("<Key>", key)

MyTitle = tk.Label(window, text="Random Number Generator", font="Helvetica 16 bold")
MyTitle.pack()

# prompt
# ---------------
prompt = tk.Label(text="Enter dice size (1-20)")
prompt.pack()

# Form
# ---------------
form = tk.Entry(window, text="type here")
form.pack()

if (form.get() != ''):
    diceMax = int(form.get())


# Button
# ---------------
MyButton = tk.Button(window, text="OK", command=RandomNumber)
MyButton.pack()

# tkinter auto sets things to 0,0 of the grid
#prompt.grid(column=0,row=0)


dice_thrown = tk.Label(window, font="Helvetica 16 bold")
dice_thrown.pack()


window.mainloop()
