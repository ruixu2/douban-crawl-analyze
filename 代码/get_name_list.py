import os
import re


def get_name_list():
    file_list = os.listdir()
    name_list = []
    regex = re.compile('txt版')
    for name in file_list:
        if regex.search(string=name):
            name_list.append(name)
    # print(name_list)
    return name_list
