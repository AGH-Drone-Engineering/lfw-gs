#!/usr/bin/python
# -*- coding: utf-8 -*-
import tkinter as Tk
from itertools import count
import socket
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
import multiprocessing

root = Tk.Tk()


class Slider:
    def __init__(self, x_slider: int, y_slider: int, min_range_slider: int, max_range_slider: int, x_button: int,
                 y_button: int, name_button: str, on_press):
        self.btn = None
        self.slider = None
        self.x_slider = x_slider
        self.y_slider = y_slider
        self.x_button = x_button
        self.y_button = y_button
        self.name_button = name_button
        self.min_range_slider = min_range_slider
        self.max_range_slider = max_range_slider
        self.on_press = on_press

    def slider_gener(self):
        self.slider = Tk.Scale(root, from_=self.min_range_slider, to=self.max_range_slider, orient=Tk.HORIZONTAL)
        self.slider.place(x=self.x_slider, y=self.y_slider)

    def slider_button(self):
        self.btn = Tk.Button(root, text=self.name_button, command=self.slider_callback)
        self.btn.place(x=self.x_button, y=self.y_button)

    def slider_callback(self):
        # print(self.name_button + str(';') + str(self.slider.get()))
        self.on_press(self.name_button + str(';') + str(self.slider.get()) + "\n")


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


class Gui:
    def __init__(self):
        # super().__init__(x_box, y_box, width, x_button, y_button)
        self.x_list_right_motor = []
        self.y_list_right_motor = []
        self.x_list_left_motor = []
        self.y_list_left_motor = []
        self.socket = None

    def add_data_to_gui(self, data_check, name_x: str, x_list: list, y_list: list):
        start_world = data_check.find(name_x)
        len_specific_name = len(name_x)
        start = len_specific_name + start_world
        first_value = data_check[:start_world].isnumeric()
        second_value = data_check[start:-1].isnumeric()
        if first_value == 1 and second_value == 1:
            x_value = float(data_check[:start_world])
            x_list.append(x_value)
            y_value = float(data_check[start:])
            y_list.append(y_value)
        else:

            print('Wrong start type of data, not flat or int')

    def recognize_data(self, given_data):
        # data = '192;angle;8225'
        used_names = (';left_motor;', ';right_motor;', ';angle;')

        if given_data.find(used_names[0]) > 0:
            self.add_data_to_gui(given_data, used_names[0], self.x_list_left_motor, self.y_list_left_motor)
        elif given_data.find(used_names[1]) > 0:
            self.add_data_to_gui(given_data, used_names[1], self.x_list_right_motor, self.y_list_right_motor)
        elif given_data.find(used_names[2]) > 0:
            self.add_data_to_gui(given_data, used_names[2], self.x_list_right_motor, self.y_list_right_motor)
        else:
            print("Non expected type of data")

    def connection(self, host_id, connection_break=False):
        if connection_break:
            print("Thread killed")
        else:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    self.socket = s
                    s.connect((host_id, 8888))
                    s.sendall(b"#Connect to the server\n")
                    while True:
                        data = s.recv(1024)
                        data = data.decode("utf-8")
                        print(data)
                        self.recognize_data(data)

                    s.close()
                    self.socket = None
            except:
                raise "Connection error"

    def send_message(self, message):
        self.socket.sendall(bytes(message, 'utf-8'))

    def animate(self, i):
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
        ax1.plot(self.x_list_right_motor, self.y_list_right_motor, label='PID reaction')
        ax1.plot(self.x_list_left_motor, self.y_list_left_motor, label='Angle')
        ax1.legend()

        ax2.plot(self.x_list_right_motor, self.y_list_right_motor, label='2 engine')
        ax2.plot(self.x_list_left_motor, self.y_list_left_motor, label='1 engine')
        ax2.legend()


class Main:

    def main(self):
        root.geometry("600x550")
        root.resizable(width=False, height=False)
        root.title("LineFollower controller")

        # graph 1
        canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
        canvas.get_tk_widget().place(x=0, y=0)
        # Create two subplots in row 1 and column 1, 2
        plt.gcf().subplots(1, 2)

        graphs = Gui()

        connect_IP = Box(x_box=240, y_box=0, width=30, x_button=290, y_button=20, on_press=0, graphs=graphs)
        connect_IP.disconnected()
        connect_IP.box_gener()
        connect_IP.box_button_con()
        time.sleep(0.5)
        ani = FuncAnimation(plt.gcf(), graphs.animate, interval=100, blit=False)

        slider_P_reg = Slider(x_slider=100, y_slider=480, min_range_slider=0, max_range_slider=100, x_button=140,
                              y_button=520,
                              name_button='Set P', on_press=graphs.send_message)
        slider_P_reg.slider_gener()
        slider_P_reg.slider_button()

        slider_P_reg = Slider(x_slider=400, y_slider=480, min_range_slider=0, max_range_slider=100, x_button=440,
                              y_button=520,
                              name_button='Set D', on_press=graphs.send_message)
        slider_P_reg.slider_gener()
        slider_P_reg.slider_button()



        root.mainloop()


if __name__ == '__main__':
    main = Main()
    main.main()
