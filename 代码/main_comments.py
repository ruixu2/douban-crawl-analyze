import threading
# 不知道什么原因，导入不了，所以集合在一个py文件里面
import time
import random
import requests
from bs4 import BeautifulSoup
import pymysql
import re
import csv

head = 'https://movie.douban.com/subject/'
middle = '/comments?start='
zx_tail = '&limit=20&sort=time&status=P&percent_type='
zr_tail = '&limit=20&sort=new_score&status=P&percent_type='
names = []
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
}
# https://movie.douban.com/subject/26647117/comments?start=0&limit=20&sort=new_score&status=P&percent_type=h
zr_urls = ['最热']
zx_urls = ['最新']
zrh_urls = ['最热评分高']
zrm_urls = ['最热评分一般']
zrl_urls = ['最热评分差']


def createUrls(num_list):
    for num in num_list:  # 读取的行数
        for i in range(0, 100, 20):
            zrh_urls.append(head + str(num) + middle + str(i) + zr_tail + 'h')  # 构建最热默认
            zrm_urls.append(head + str(num) + middle + str(i) + zr_tail + 'm')  # 构建最热默认
            zrl_urls.append(head + str(num) + middle + str(i) + zr_tail + 'l')  # 构建最热默认


def read_num():
    list = []
    with open('../txt/编号新.txt', mode='r', encoding='utf-8') as f:
        result = f.readlines()
        for i in range(1, len(result), 2):
            list.append(result[i].strip('\n'))
    return list


def get_comments_to_mysql(urls):
    global sort_name  #
    sort_name = urls[0]  # 从第一个元素得到分类方式
    del urls[0]  # 删掉
    for url in urls:
        conn = pymysql.connect(host='localhost', user="root", password='0823')
        cursor = conn.cursor()
        cursor.execute('create database if not exists comment;')
        cursor.execute('use comment;')
        comment_list = []
        try:
            resp = requests.get(url=url, headers=header)
            time.sleep(4)  # 亲测大概4000条数据被封ip，这样的话不会封ip
            print('正在请求 ' + url)
        except requests.RequestException:
            print(requests.RequestException.request)
            continue
        resp.encoding = 'utf-8'  # 使用utf-8编码
        soup = BeautifulSoup(resp.text, 'lxml')
        global video_name
        video_name = soup.find(name='title').string
        global result
        result = soup.find_all(name='p')  # 所有的评论
        for item in result[2:len(result) - 7]:
            comment_list.append(item.get_text())  # 找到所有p标签下的文本，不迭代
        if urls.index(url) % 5 == 0:  # with open(video_name + sort_name + '.csv', mode='w',
            cursor.execute('create table if not exists {} (content text);'.format(video_name))
        for comment in comment_list:
            cursor.execute('insert into {} content value {}'.format(video_name, comment))
        conn.commit()
        cursor.close()
        print("--------------------")


def get_comments(urls):
    for url in urls[1:]:
        try:
            resp = requests.get(url=url, headers=header, proxies={'http': '110.185.227.236'})
            time.sleep(random.randint(3, 6))  # 亲测大概4000条数据被封ip，这样的话不会封ip
            print('正在请求 ' + url)
            if resp.status_code != 200:
                print("啊哈哈哈，ip又被封了，等一会我们再来")
                time.sleep(5)
                resp = requests.get(url=url, headers=header)
            resp.encoding = 'utf-8'  # 使用utf-8编码
            to_csv(urls[0], resp.text, url)
        except requests.RequestException:
            time.sleep(4)  # 亲测大概4000条数据被封ip，这样的话不会封ip
            resp = requests.get(url=url, headers=header)
            print('出现了错误，正在重新请求 ' + url)
            resp.encoding = 'utf-8'  # 使用utf-8编码
            to_csv(urls[0], resp.text, url)


def to_csv(sort, text, url):
    mode = 'a'
    if "start=0" in url:
        mode = 'w'
    comment_list = []
    soup = BeautifulSoup(text, 'lxml')
    video = soup.find(name='title').string
    results = re.findall(pattern='<p class="">.*?</p>', string=text, flags=re.S)  # 所有的评论
    for item in results:
        ahhh = BeautifulSoup(item, 'lxml')
        print("ahhh:" + ahhh.get_text())
        comment_str = ahhh.get_text()
        comment_list.append(comment_str)  # 找到所有p标签下的文本，不迭代
    print("video:" + video)
    print("sort:" + sort)
    with open("../txt/" + str(video) + str(sort) + ".txt", mode=mode, encoding='utf-8') as f:
        for comment in comment_list:
            f.write(comment)
        f.close()
    with open("../csv/" + str(video) + str(sort) + ".csv", mode=mode, encoding='utf-8') as f:
        for comment in comment_list:
            f.write(comment)
        f.close()
    print("--------------------")


num_list = read_num()
createUrls(num_list)
print("评分高开始======")
t1 = threading.Thread(target=get_comments, args=(zrh_urls,))
print("评分一般开始======")
t2 = threading.Thread(target=get_comments, args=(zrm_urls,))
print("评分低开始======")
t3 = threading.Thread(target=get_comments, args=(zrl_urls,))
t1.start()
t2.start()
t3.start()
t1.join()
t2.join()
t3.join()
