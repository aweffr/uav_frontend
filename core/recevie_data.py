import socket
import struct
from datetime import datetime
from sqlalchemy import Column, String, create_engine, Integer, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json
import requests

# 创建对象的基类
Base = declarative_base()


# 定义飞机回传数据对象
class Info(Base):
    __tablename__ = "info"
    id = Column(Integer, primary_key=True)
    jing_du = Column(Float)
    wei_du = Column(Float)
    height = Column(Float)
    chou_yang = Column(Float)
    pm25 = Column(Float)
    wen_du = Column(Float)
    shi_du = Column(Float)

    def __repr__(self):
        return "<Info jing_du=%f wei_du=%f height=%f" % (self.jing_du, self.wei_du, self.height)


def connect_db(url, refresh=False):
    engine = create_engine(url)
    if refresh:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return engine, session


class SendToServer:
    def __init__(self, url):
        self.url = url

    def send(self, data):
        r = requests.post(self.url, json=json.dumps(data))
        print(r.status_code)


def revice_data_service(host, port, db_session=None, client=None):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("create socket succeed!")

        sock.bind((host, port))
        print("bind socket succeed!")

        sock.listen(10)
        print("listen succeed!")

    except Exception as e:
        print("init socket err!")
        return

    while True:
        try:
            time_string = datetime.now().strftime("%H-%M-%S")
            print("listen for client...")
            conn, addr = sock.accept()
            print("get client", conn, addr)

            conn.settimeout(5)
            szBuf = conn.recv(1024)

            s = szBuf.decode("utf-8")
            s = list(map(float, s.split()))

            print("Service succeed at %s" % time_string)
            print("unpacked:", s)

            jing_du = s[2]
            wei_du = s[3]
            chou_yang = s[5]

            if db_session is not None:
                try:
                    info = Info(jing_du=jing_du, wei_du=wei_du, height=0.0, chou_yang=chou_yang)
                    print(info)
                    db_session.add(info)
                    db_session.commit()
                except Exception as e:
                    print("database insert error", e)

            if client is not None:
                message = {"jing_du": jing_du, "wei_du": wei_du, "height": 0.0, "chou_yang": chou_yang}
                client.send(message)

            conn.close()
            print("end of sevice")

        except Exception as e:
            time_string = datetime.now().strftime("%H-%M-%S")
            print("Service error at %s" % time_string)


if "__main__" == __name__:
    client = SendToServer(url="http://localhost:5000/receive_data_from_uav")
    revice_data_service(host="0.0.0.0", port=5050, client=client)
