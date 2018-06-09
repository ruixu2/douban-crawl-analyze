from aip import AipNlp
import os
import random
import time
import csv


class SentimentClassify(object):
    def __init__(self, app_id, api_key, secret_key):
        self.APP_ID = app_id
        # '11341811'
        self.API_KEY = api_key
        # 'H8XeFrAPOQxn2UvebBwAPXCx'
        self.SECRET_KEY = secret_key

    def sentiment_classify(self, texts, name):
        if os.path.exists("../csv/情感分析" + name.strip('.txt') + ".csv"):
            return
        client = AipNlp(appId=self.APP_ID, apiKey=self.API_KEY, secretKey=self.SECRET_KEY)
        with open("../csv/情感分析" + name.strip('.txt') + ".csv", mode='w') as f:
            csv_write = csv.writer(f)
            csv_write.writerow(["分析文本", "积极情感", "消极情感", "sentiment", "confidence"])
            for item in texts:
                try:
                    result = client.sentimentClassify(text=item)
                    print("正在分析：" + item)
                    csv_write.writerow([result['text'], result['items'][0]["positive_prob"],
                                        result['items'][0]["negative_prob"], result['items'][0]["sentiment"],
                                        result['items'][0]["confidence"]])
                    print("正在写入：" + result['text'] + "\t" + str(result['items'][0]["positive_prob"]) + "\t" + str(
                        result['items'][0]["negative_prob"]) + "\t" + str(result['items'][0]["sentiment"]) + "\t" + str(
                        result['items'][0]["confidence"]))
                    time.sleep(random.randint(0, 1))
                    print("影评：" + name)
                except BaseException as e:
                    print("error:" + str(e))
                    continue

    def get_comment_content(self, filenames):
        for name in filenames:
            contents = []
            if "编号" in name:
                continue
            with open("../txt/" + name, mode='r', encoding='utf-8') as f:
                for item in f.readlines():
                    if item is None:
                        continue
                    contents.append(item)
                f.close()
            self.sentiment_classify(contents, name)

    def get_filename_list(self):
        filenames = os.listdir("../txt/")
        return filenames


if __name__ == '__main__':
    ahhh = SentimentClassify(app_id='11341811', api_key="H8XeFrAPOQxn2UvebBwAPXCx",
                             secret_key="2bhd8OuDsm5TppzPYpZG1XPS7vGNSsAI")
    filename_list = ahhh.get_filename_list()
    ahhh.get_comment_content(filename_list)
