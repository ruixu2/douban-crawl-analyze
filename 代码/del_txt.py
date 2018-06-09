import os

file_list = os.listdir()
for file in file_list:
    if ".txt" in file:
        os.remove(file)
