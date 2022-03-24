from tkinter import *

win = Tk()

def btn1():
  print("I Don't Know Your Name")

button1 =  Button(win, text="Click Me To Print SomeThing", command=btn1)

button1.pack()
win.mainloop()