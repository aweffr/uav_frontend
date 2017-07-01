import struct
import socket

ip_port = ("127.0.0.1", 5050)

data = "0.0 1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0".encode("utf-8")

s = socket.socket()

s.connect(ip_port)
s.send(data)
s.close()