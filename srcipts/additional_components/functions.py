#!/usr/bin/python
# -*- coding: utf-8 -*-
import tkinter as Tk
from gui import root
import threading


class Box:
    def __init__(self, x_box: int, y_box: int, width: int, x_button: int, y_button: int, on_press, graphs):
        self.close = None
        self.thread1 = None
        self.label = Tk.Button()
        self.button_dis = None
        self.button_con = None
        self.box = None
        self.x_box = x_box
        self.y_box = y_box
        self.x_button = x_button
        self.y_button = y_button
        self.width = width
        self.on_press = on_press
        self.graphs = graphs

    def box_gener(self):
        self.box = Tk.Entry(root, width=self.width)
        self.box.insert(0, 'Connect with IP')
        self.box.place(x=self.x_box, y=self.y_box)

    def box_button_con(self):
        self.button_con = Tk.Button(root, text='Connected', command=self.box_callback)
        self.button_con.place(x=self.x_button, y=self.y_button)

    def box_button_dis(self):
        self.button_dis = Tk.Button(root, text='Disconnect', command=self.disconnected_callback)
        self.button_dis.place(x=500, y=-2)

    def box_callback(self):
        self.label.destroy()
        connected_message = "You're connected: " + str(self.box.get())
        self.label = Tk.Label(root, text=connected_message)
        self.label.place(x=0, y=0)
        self.close = False
        self.thread1 = threading.Thread(target=self.graphs.connection, args=[self.box.get()])
        self.thread1.start()
        self.button_con.destroy()
        self.box.destroy()


    def disconnected(self):
        self.label.destroy()
        connected_message = "You're disconnected"
        self.label = Tk.Label(root, text=connected_message)
        self.label.place(x=0, y=0)


    def disconnected_callback(self):
        self.label.destroy()
        connected_message = "You're disconnected"
        self.label = Tk.Label(root, text=connected_message)
        self.label.place(x=0, y=0)
        print("Finish disconnect button")