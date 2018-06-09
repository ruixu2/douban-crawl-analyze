import os


def del_excess(path):
    file_list = os.listdir(path)
    for file in file_list:
        if "txt版" in file:
            os.remove(path + file)
        if "词频分析词频分析" in file:
            os.remove(path + file)
        # if ".csv.csv" in file:
        #     os.remove(path + file)


del_excess('../txt/')
