#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket


# ncat -l 8888
def add_data_to_gui(data_check, name_x: str, x_list: list, y_list: list):
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
        print(data_check[:start_world].isnumeric(), data_check[start:].isnumeric())
        print('Wrong start type of data, not flat or int')


def recognize_data(given_data):
    # data = '192;angle;8225'
    used_names = (';left_motor;', ';right_motor;', ';angle;')

    if given_data.find(used_names[0]) > 0:
        add_data_to_gui(given_data, used_names[0], x_list_left_motor, y_list_left_motor)
    elif given_data.find(used_names[1]) > 0:
        add_data_to_gui(given_data, used_names[1], x_list_right_motor, y_list_right_motor)
    elif given_data.find(used_names[2]) > 0:
        add_data_to_gui(given_data, used_names[2], x_list_right_motor, y_list_right_motor)
    else:
        print("Non expected type of data")

    print(x_list_left_motor, y_list_left_motor, x_list_right_motor, y_list_right_motor)


x_list_left_motor, y_list_left_motor = [], []
x_list_right_motor, y_list_right_motor = [], []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('localhost', 8888))
    s.sendall(b"Connect to the server")
    while True:
        data = s.recv(1024)
        data = data.decode("utf-8")
        print(data)
        recognize_data(data)
