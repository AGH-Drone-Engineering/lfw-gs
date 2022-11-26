#!/usr/bin/python
# -*- coding: utf-8 -*-
import tkinter as Tk
import socket
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
import os

root = Tk.Tk()

x_angle_global = []
y_angle_global = []
P_global = []
D_global = []
velocity = []

class Button:
    def __init__(self, x_button: int, y_button: int, name_button: str):
        self.button = None
        self.x_button = x_button
        self.y_button = y_button
        self.name_button = name_button

    def button_generation(self):
        self.button = Tk.Button(root, text=self.name_button, command=self.button_callback)
        self.button.place(x=self.x_button, y=self.y_button)

    def button_callback(self):
        dir_path = r'../data'

        numer_file = len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))])
        numer_file += 1

        file_name = '../data/angle_data' + str(numer_file) + '.txt'
        with open(file_name, 'w') as f:
            for i, j in zip(x_angle_global, y_angle_global):
                f.write(str(i) + ',' + str(j))
                f.write('\n')

        file_name_pid = '../data/pid_settings' + str(numer_file) + '.txt'
        with open(file_name_pid, 'w') as f:
            for i, j, h in zip(P_global, D_global, velocity):
                f.write('P: ' + str(i) + ',' + 'D: ' + str(j) + ',' + str(h))
                f.write('\n')


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
        self.on_press(self.name_button + str(';') + str(self.slider.get()) + "\n")
        if self.name_button == 'Set P':
            P_global.append(self.slider.get())
        elif self.name_button == 'Set D':
            D_global.append(self.slider.get())
        else:
            pass

class Box2:
    def __init__(self, x_box: int, y_box: int, width: int, x_button: int, y_button: int, on_press, box_name: str,
                 button_name: str):
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
        self.box_name = box_name
        self.button_name = button_name

    def box_gener(self):
        self.box = Tk.Entry(root, width=self.width)
        self.box.insert(0, self.box_name)
        self.box.place(x=self.x_box, y=self.y_box)

    def box_button_con(self):
        self.button_con = Tk.Button(root, text=self.button_name, command=self.box_callback)
        self.button_con.place(x=self.x_button, y=self.y_button)

    def box_callback(self):
        self.on_press(self.button_name + str(';') + str(self.box.get()) + "\n")
        if self.button_name == 'Set P':
            P_global.append(self.box.get())
        elif self.button_name == 'Set D':
            D_global.append(self.box.get())
        elif 'Set forward':
            velocity.append(self.box.get())
        else:
            pass

class Box:
    def __init__(self, x_box: int, y_box: int, width: int, x_button: int, y_button: int, on_press, graphs, box_name: str):
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
        self.box_name = box_name

    def box_gener(self):
        self.box = Tk.Entry(root, width=self.width)
        self.box.insert(0, self.box_name)
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
        self.x_list_right_motor = []
        self.y_list_right_motor = []
        self.x_list_left_motor = []
        self.y_list_left_motor = []
        self.x_angle = []
        self.y_angle = []
        self.x_pid_response = []
        self.y_pid_response = []
        self.socket = None

    def add_data_to_gui(self, data_check, name_x: str, x_list: list, y_list: list):
        start_world = data_check.find(name_x)
        len_specific_name = len(name_x)
        start = len_specific_name + start_world

        first_value = data_check[:start_world]
        second_value = data_check[start:]

        try:
            x_value = float(first_value)
            y_value = float(second_value)
            x_list.append(x_value)
            y_list.append(y_value)
            del x_list[:-100]
            del y_list[:-100]

            if data_check.find(';angle;') > 0:
                x_angle_global.append(x_value)
                y_angle_global.append(y_value)

        except ValueError:

            print('Wrong start type of data, not flat or int', data_check)

    def recognize_data(self, given_data):
        # data = '192;angle;8225'
        used_names = (';left_motor;', ';right_motor;', ';angle;', ';pid_response;')

        if given_data.find(used_names[0]) > 0:
            self.add_data_to_gui(given_data, used_names[0], self.x_list_left_motor, self.y_list_left_motor)
        elif given_data.find(used_names[1]) > 0:
            self.add_data_to_gui(given_data, used_names[1], self.x_list_right_motor, self.y_list_right_motor)
        elif given_data.find(used_names[2]) > 0:
            self.add_data_to_gui(given_data, used_names[2], self.x_angle, self.y_angle)
        elif given_data.find(used_names[3]) > 0:
            self.add_data_to_gui(given_data, used_names[3], self.x_pid_response, self.y_pid_response)
        elif given_data[0] == '#':
            print(given_data)
        else:
            pass

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
                        # print(data)
                        for line in data.strip().split('\n'):
                            self.recognize_data(line)

                    s.close()
                    self.socket = None
            except:
                raise "Connection error"

    def send_message(self, message):
        print(message)
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
        # ax2.axis()
        # ax2.set(ylim=(0, 100))
        # Plot new data
        ax1.plot(self.x_pid_response, self.y_pid_response, label='PID reaction')
        ax1.plot(self.x_angle, self.y_angle, label='Angle')
        ax1.legend()

        ax2.plot(self.x_list_right_motor, self.y_list_right_motor, label='R engine')
        ax2.plot(self.x_list_left_motor, self.y_list_left_motor, label='L engine')
        ax2.legend()


class Main:

    def main(self):
        root.geometry("600x600")
        root.resizable(width=False, height=False)
        root.title("LineFollower controller")

        # graph 1
        canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
        canvas.get_tk_widget().place(x=0, y=0)
        # Create two subplots in row 1 and column 1, 2
        plt.gcf().subplots(1, 2)

        graphs = Gui()

        connect_IP = Box(x_box=240, y_box=0, width=30, x_button=290, y_button=20, on_press=0, graphs=graphs,
                         box_name='192.168.4.1')
        connect_IP.disconnected()
        connect_IP.box_gener()
        connect_IP.box_button_con()
        time.sleep(0.5)
        ani = FuncAnimation(plt.gcf(), graphs.animate, interval=100, blit=False)

        # slider_P_reg = Slider(x_slider=440, y_slider=480, min_range_slider=0, max_range_slider=1000, x_button=550,
        #                       y_button=495, name_button='Set P', on_press=graphs.send_message)
        # slider_P_reg.slider_gener()
        # slider_P_reg.slider_button()

        box_p_reg = Box2(x_box=460, y_box=500, width=10, x_button=550, y_button=495, on_press=graphs.send_message,
                         button_name='Set P',box_name='470')
        box_p_reg.box_gener()
        box_p_reg.box_button_con()

        # slider_D_reg = Slider(x_slider=440, y_slider=515, min_range_slider=0, max_range_slider=1000, x_button=550,
        #                       y_button=530, name_button='Set D', on_press=graphs.send_message)
        # slider_D_reg.slider_gener()
        # slider_D_reg.slider_button()

        box_d_reg = Box2(x_box=460, y_box=530, width=10, x_button=550, y_button=530, on_press=graphs.send_message,
                         button_name='Set D', box_name='17000')
        box_d_reg.box_gener()
        box_d_reg.box_button_con()

        button_save_date = Button(460, 570, 'save_data')
        button_save_date.button_generation()

        # velocity = Slider(x_slider=10, y_slider=480, min_range_slider=0, max_range_slider=1000, x_button=120,
        #                       y_button=495,
        #                       name_button='Set forward', on_press=graphs.send_message)
        # velocity.slider_gener()
        # velocity.slider_button()
        #
        box_v = Box2(x_box=25, y_box=500, width=10, x_button=120, y_button=495, on_press=graphs.send_message,
                         button_name='Set forward', box_name='600')
        box_v.box_gener()
        box_v.box_button_con()

        enable = Slider(x_slider=10, y_slider=515, min_range_slider=0, max_range_slider=1, x_button=120,
                              y_button=530,
                              name_button='Enable', on_press=graphs.send_message)
        enable.slider_gener()
        enable.slider_button()

        # turbin = Slider(x_slider=10, y_slider=550, min_range_slider=0, max_range_slider=255, x_button=120,
        #                       y_button=565,
        #                       name_button='Turbine', on_press=graphs.send_message)
        # turbin.slider_gener()
        # turbin.slider_button()

        box_t = Box2(x_box=25, y_box=570, width=10, x_button=120, y_button=565, on_press=graphs.send_message,
                         button_name='Turbine',box_name='255')
        box_t.box_gener()
        box_t.box_button_con()

        root.mainloop()


if __name__ == '__main__':
    main = Main()
    main.main()
