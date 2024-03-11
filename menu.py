
from asyncio import windows_events
from lib2to3.pgen2.token import STAR
from operator import truediv
from sqlite3 import Row
import tkinter
from tkinter.tix import COLUMN, ROW
from tkinter import*
from tkinter.ttk import *
from tkinter import messagebox
import os
from tkinter import Button
from PIL import Image, ImageTk
import main
import threading
check = False


def canceclick():
    try:
        window.destroy()
        Tk.tk = None
        game.falserunig()
        window.tk = None
        exit()
    except:
        pass


def newclick():
    game.checkwin = 0
    game.secon = 120
    AI.landithu = 0
    window.destroy()
    if(game.chedochoi == '1v1'):
        window.protocol(game.playnew())
    else:
        window.protocol(game.playnewAI())


def play():

    global window
    window = Tk()
    window.geometry("210x230")
    window.resizable(width=False, height=False)
    window.title("Menu")
    window.iconbitmap(".\img\Iconka-Saint-Whiskers-Cat-cupid-love.ico")
    window.eval('tk::PlaceWindow . center')
    img = Image.open(".\img\caro.png")
    img = img.resize((210, 230))
    img = ImageTk.PhotoImage(img)
    panel = Label(window, image=img)
    panel.image = img
    panel.pack()
    btnctinu = Button(window, text="Game mới", width=20, height=2,
                      command=newclick, activebackground="#FF6347", bg="#00BFFF")
    btnctinu.place(x=30, y=30)

    btnnew = Button(window, text="Save", width=20, height=2,
                    command=newclick, activebackground="#FF6347", bg="#00BFFF")
    btnnew.place(x=30, y=90)

    btnsave = Button(window, text="Exit", width=20, height=2,
                     command=canceclick, activebackground="#FF6347", bg="#00BFFF")
    btnsave.place(x=30, y=150)
    window.mainloop()
