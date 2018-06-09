# encoding='gbk'
import requests
import re
from bs4 import BeautifulSoup
header = {'Content-Type': 'application/json; charset=UTF-8'}
init_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=【官网获取的AK】&client_secret=【官网获取的SK】'
AK = 'H8XeFrAPOQxn2UvebBwAPXCx'
SK = '2bhd8OuDsm5TppzPYpZG1XPS7vGNSsAI'
init_url = re.sub(pattern='【官网获取的AK】', repl=AK, string=init_url, count=1)
init_url = re.sub(pattern='【官网获取的SK】', repl=SK, string=init_url, count=1)
# print(init_url)
access_token = requests.get(url=init_url, headers=header).content
# soup = BeautifulSoup(access_token, 'lxml')
# print(soup.p.string)
print(access_token)