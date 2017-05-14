import shelve
import os
import json
from random import randint, random

def too_close(data, x, y):
    for xx, yy in data:
        if abs(xx - x) + abs(yy -x) < 0.0001:
            return True
    return False

def generate_ramdom_walk(start_x, start_y):
    data = []
    f = open("../static/data/pm25_data.json", "w", encoding="utf-8")
    string_list = []
    tmp_x = start_x
    tmp_y = start_y
    for i in range(50):
        s = """{
                    "coord": [%.6f, %.6f],
                    "elevation": %d
                }""" % (tmp_x, tmp_y, randint(45, 65))
        string_list.append(s)
        data.append((tmp_x, tmp_y))
        while True:
            tmp_xx = tmp_x + 0.0003 * (random() - 0.48)
            tmp_yy = tmp_y + 0.0003 * (random() - 0.48)
            if too_close(data, tmp_xx, tmp_yy):
                continue
            else:
                tmp_x = tmp_xx
                tmp_y = tmp_yy
                break

    f.writelines("[[" + ",".join(string_list) + "]]")
    f.close()


if __name__ == "__main__":
    generate_ramdom_walk(121.452365, 31.036464)
