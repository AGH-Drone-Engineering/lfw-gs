#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *

root = Tk()

e = Entry(root, width=50)
e.pack()
e.insert(0, 'Enter value')

def click():
    label = Label(root, text=e.get())
    label.pack()


button = Button(root, text='Click me', command=click, fg='blue', bg='red', padx=20, pady=10)  # jest komenda padx i pady które definiuja wielkosc buttona
button.pack()


slider = Scale(root, from_=0, to=100, orient=HORIZONTAL)
slider.pack()



def slide():
    my_lebel = Label(root, text=slider.get()).pack()
    # print(slider.get())

btn = Button(root, text="Refresh variable", command=slide).pack()
root.mainloop()
