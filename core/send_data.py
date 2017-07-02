from random import random
import struct
import socket

ip_port = ("aweffr.win", 5050)

data = "0.00000,0.00000,-0.00341,106.000000,0.000000,25.900000,64.300000".encode("utf-8")



for i in range(100):
    s = socket.socket()
    s.connect(ip_port)
    data = [str(100 * random()) for j in range(7)]
    data = ",".join(data).encode("utf-8")
    s.send(data)
    s.close()
