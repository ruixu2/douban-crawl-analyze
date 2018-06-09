import jieba.analyse
import os
import csv


def get_filename_list():
    f_list = os.listdir("../txt/")
    low_feed_list = []
    for name in f_list:
        if "残团" in name:
            low_feed_list.append(name)
        if "大会师" in name:
            low_feed_list.append(name)
        if "狼兵吼" in name:
            low_feed_list.append(name)
    print(low_feed_list)
    return low_feed_list


def count_it(word, all_words):
    num = 0
    for item in all_words:
        if word == item:
            num += 1
    return num


def get_counts(filename_list):
    for filename in filename_list:
        with open('../txt/' + filename, mode='r', encoding='utf-8') as f:
            text = f.readlines()
            all_words = jieba.lcut(str(text))
            word_list = jieba.analyse.extract_tags(sentence=str(text), topK=50, withWeight=True)
            with open("../csv/" + "词频分析" + filename.strip(".txt") + ".csv", mode="w", encoding='gbk') as fn:
                csv_write = csv.writer(fn)
                csv_write.writerow(["词语", "权重", "词频"])
                for word in word_list:
                    num = count_it(word[0], all_words)
                    csv_write.writerow([word[0], word[1], num])
                fn.close()
            f.close()
        print("完成了" + filename)


file_names = get_filename_list()
get_counts(file_names)
