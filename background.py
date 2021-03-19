import tkinter as tk
from tkinter import PhotoImage, Label

root = tk.Tk()
root.geometry("1280x1024")

filename = PhotoImage(file = "C:/Users/Work/Desktop/NATASHA-LCD/aa.png")
background_label = Label(root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


root.mainloop()