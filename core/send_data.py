from random import random
import struct
import socket
import time

ip_port = ("aweffr.win", 5050)
# ip_port = ("127.0.0.1", 5050)

data = "0.00000,0.00000,-0.00341,106.000000,0.000000,25.900000,64.300000".encode("utf-8")

for i in range(240):
    try:
        s = socket.socket()
        s.connect(ip_port)
        data = [str(100 * random()) for j in range(7)]
        data = ",".join(data).encode("utf-8")
        s.send(data)
        print(data)
        s.close()
        time.sleep(1)
    except Exception as e:
        print("#BUG", e)
