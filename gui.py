#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import tkinter as Tk
from itertools import count

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Gui:
    def __init__(self):
        self.x_vals = []
        self.y_vals = []
        # values for second graph
        self.y_vals2 = []
        self.y_vals3 = []
        self.index = count()

    def animate(self, i):
        # Generate values
        self.x_vals.append(next(self.index))
        self.y_vals.append(random.randint(0, 5))
        self.y_vals2.append(random.randint(0, 100))
        self.y_vals3.append(random.randint(0, 100))

        # Get all axes of figure
        ax1, ax2 = plt.gcf().get_axes()
        # Clear current data
        ax1.cla()
        ax2.cla()
        ax1.set_xlabel('Time [s]')
        ax2.set_xlabel('Time [s]')
        ax1.set_ylabel('Angle [deg]')
        ax2.set_ylabel('Power [%]')
        ax1.set_title('Steering angle')
        ax2.set_title('Power of engines')
        ax1.grid()
        ax2.grid()
        ax2.axis()
        ax2.set(ylim=(0, 100))
        # Plot new data
        ax1.plot(self.x_vals, self.y_vals, label='PID reaction')
        ax1.plot(self.x_vals, self.y_vals2, label='Angle')
        ax1.legend()

        ax2.plot(self.x_vals, self.y_vals2, label='2 engine')
        ax2.plot(self.x_vals, self.y_vals3, label='1 engine')
        ax2.legend()


class Slider:
    def __init__(self, x_slider: int, y_slider: int, min_range_slider: int, max_range_slider: int, x_button: int,
                 y_button: int, name_button: str):
        self.btn = None
        self.slider = None
        self.x_slider = x_slider
        self.y_slider = y_slider
        self.x_button = x_button
        self.y_button = y_button
        self.name_button = name_button
        self.min_range_slider = min_range_slider
        self.max_range_slider = max_range_slider

    def slider_gener(self):
        self.slider = Tk.Scale(root, from_=self.min_range_slider, to=self.max_range_slider, orient=Tk.HORIZONTAL)
        self.slider.place(x=self.x_slider, y=self.y_slider)

    def slider_button(self):
        self.btn = Tk.Button(root, text=self.name_button, command=self.slider_callback)
        self.btn.place(x=self.x_button, y=self.y_button)

    def slider_callback(self):
        print(self.slider.get())


class Box:
    def __init__(self, x_box: int, y_box: int, width: int, x_button: int, y_button: int):
        self.label = Tk.Button()
        self.button_dis = None
        self.button_con = None
        self.box = None
        self.x_box = x_box
        self.y_box = y_box
        self.x_button = x_button
        self.y_button = y_button
        self.width = width

    def box_gener(self):
        self.box = Tk.Entry(root, width=self.width)
        self.box.insert(0, 'Connect with IP')
        self.box.place(x=self.x_box, y=self.y_box)

    def box_button_con(self):
        self.button_con = Tk.Button(root, text='Connected', command=self.box_callback)
        self.button_con.place(x=self.x_button, y=self.y_button)

    def box_button_dis(self):
        self.button_dis = Tk.Button(root, text='Disconnect', command=self.disconnected)
        self.button_dis.place(x=500, y=-2)

    def box_callback(self):
        self.label.destroy()
        connected_message = "You're connected: " + str(self.box.get())
        self.label = Tk.Label(root, text=connected_message)
        self.label.place(x=0, y=0)

    def disconnected(self):
        self.label.destroy()
        connected_message = "You're disconnected"
        self.label = Tk.Label(root, text=connected_message)
        self.label.place(x=0, y=0)


root = Tk.Tk()

root.geometry("600x550")
root.resizable(width=False, height=False)
root.title("LineFollower controller")
# graph 1
canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
canvas.get_tk_widget().place(x=0, y=0)
# Create two subplots in row 1 and column 1, 2
plt.gcf().subplots(1, 2)

graphs = Gui()
ani = FuncAnimation(plt.gcf(), graphs.animate, interval=1000, blit=False)

slider_P_reg = Slider(x_slider=100, y_slider=480, min_range_slider=0, max_range_slider=100, x_button=140, y_button=520,
                      name_button='Set P')
slider_P_reg.slider_gener()
slider_P_reg.slider_button()

slider_P_reg = Slider(x_slider=400, y_slider=480, min_range_slider=0, max_range_slider=100, x_button=440, y_button=520,
                      name_button='Set D')
slider_P_reg.slider_gener()
slider_P_reg.slider_button()

connect_IP = Box(x_box=240, y_box=0, width=30, x_button=290, y_button=20)
connect_IP.disconnected()
connect_IP.box_gener()
connect_IP.box_button_con()
connect_IP.box_button_dis()

root.mainloop()
