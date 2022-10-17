#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket

# ncat -l 8888

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('localhost', 8888))
    s.sendall(b"Connect to the server")
    while True:
        data = s.recv(1024)
        print(data.decode("utf-8"))
