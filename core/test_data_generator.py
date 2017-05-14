import shelve
import os
import json
from random import randint, random


def generate_ramdom_walk(start_x, start_y):
    f = open("test_data.json", "w", encoding="utf-8")
    string_list = []
    for i in range(1000):
        s = """{
                    "coord": [%.6f, %.6f],
                    "elevation": %d
                }""" % (start_x, start_y, randint(0, 100))
        string_list.append(s)
        start_x = start_x + (random() - 0.5) * 0.001
        start_y = start_y + (random() - 0.5) * 0.001
    f.writelines("[[" + ",".join(string_list) + "]]")
    f.close()


if __name__ == "__main__":
    generate_ramdom_walk(121.450506, 31.032349)