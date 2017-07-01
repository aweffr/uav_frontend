import struct
import socket

ip_port = ("127.0.0.1", 5050)

data = "0.00000,0.00000,-0.00341,106.000000,0.000000,25.900000,64.300000".encode("utf-8")

s = socket.socket()

s.connect(ip_port)
s.send(data)
s.close()