# -*- coding: utf-8 -*-
import requests
import getSign
import time
import json
import random
import nlp
import base

class Analyze(object):
    def __init__(self):
        self.api_url = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textpolar'
        self.parser = {}
        self.app_id = 1106871017
        self.time_stamp = int(time.time())
        self.nonce_str = str(random.randint(1, 10))
        self.app_key = 'sVJuCIh9WtaF8mMh'
        self.parser['app_id'] = self.app_id
        self.parser['time_stamp'] = self.time_stamp
        self.parser['app_key'] = self.app_key
        self.parser['nonce_str'] = self.nonce_str
        self.sign = getSign.getSign(self.parser)

    def setParams(self):
        self.parser['sign'] = self.sign
        self.parser['text'] = "I am very happy!"
        params = self.parser
        del params['app_key']
        return params

    def ask_api(self, params):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        polar = []
        resp = requests.post(url=self.api_url, data=params, headers=header)
        print(resp.url)
        print(params)
        print(resp.text)
        return json.dumps(resp.text)

    def cleanData(self, relevant_parameter):
        return relevant_parameter['polar']


run = Analyze()
ans = run.ask_api(params=run.setParams())
