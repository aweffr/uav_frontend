import socket
import struct
import time

def revice_data_service(host="0.0.0.0", port=5010, shared_data_ptr=None):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        print("create socket succeed!");

        sock.bind(('0.0.0.0', 5000));
        print("bind socket succeed!");

        sock.listen(5);
        print("listen succeed!");

    except:
        print("init socket err!");

    while True:
        try:
            print("listen for client...");
            conn, addr = sock.accept();
            print("get client");
            print(addr);

            conn.settimeout(5);
            szBuf = conn.recv(1024);

            s = struct.Struct("ffffff")
            unpacked_data = s.unpack(szBuf)
            print("Service succeed at %s" % time.strftime("%H-%M-%S"))
            print("unpacked:", unpacked_data)

            jing_du = unpacked_data[2]
            wei_du = unpacked_data[3]
            ozone_value = unpacked_data[5]

            conn.close();
            print("end of sevice");
        except Exception as e:
            print("Service error at %s" % time.strftime("%H-%M-%S"), time.time())


if "__main__" == __name__:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        print("create socket succeed!");

        sock.bind(('0.0.0.0', 5000));
        print("bind socket succeed!");

        sock.listen(8);
        print("listen succeed!");

    except:
        print("init socket err!");

    while True:
        try:
            print("listen for client...");
            conn, addr = sock.accept();
            print("get client");
            print(addr);

            conn.settimeout(5);
            szBuf = conn.recv(1024);

            s = struct.Struct("ffffff")
            unpacked_data = s.unpack(szBuf)
            print("Service succeed at %s" % time.strftime("%H-%M-%S"))
            print("unpacked:", unpacked_data)

            conn.close();
            print("end of sevice");
        except Exception as e:
            print("Service error at %s" % time.strftime("%H-%M-%S"), time.time())