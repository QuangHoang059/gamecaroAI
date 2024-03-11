

from operator import truediv
from tkinter import*
from tkinter.ttk import *
from tkinter import Button
from PIL import Image, ImageTk


class Option():
    def __init__(self):
        self.chedo = 0
        self.window = Tk()
        self.window.geometry("210x280")
        self.window.resizable(width=False, height=False)
        self.window.title("Start")
        self.window.iconbitmap(
            ".\img\Iconka-Saint-Whiskers-Cat-cupid-love.ico")
        self.window.eval('tk::PlaceWindow . center')

    def newClick(self):
        self.chedo = 2
        self.window.destroy()

    def newAI(self):
        self.chedo = 1
        self.window.destroy()

    def Star(self):

        img = Image.open(".\img\caro.png")
        img = img.resize((210, 280))
        img = ImageTk.PhotoImage(img)
        panel = Label(self.window, image=img)
        panel.pack()
        btnnew = Button(self.window, text="Chơi với máy", width=20, height=2,
                        command=self.newAI, activebackground="#FF6347", bg="#00BFFF")
        btnnew.place(x=30, y=30)
        btnctinu = Button(self.window, text="1 vs 1", width=20, height=2,
                          command=self.newClick, activebackground="#FF6347", bg="#00BFFF")
        btnctinu.place(x=30, y=90)
        btnnew = Button(self.window, text="Save", width=20, height=2,
                        command=None, activebackground="#FF6347", bg="#00BFFF")
        btnnew.place(x=30, y=150)

        btnsave = Button(self.window, text="Exit", width=20, height=2,
                         command=None, activebackground="#FF6347", bg="#00BFFF")
        btnsave.place(x=30, y=210)
        self.window.mainloop()
