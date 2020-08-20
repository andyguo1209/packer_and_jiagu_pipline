#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@Time : 2020/8/20 下午10:32
#@Author : guozhenhua
#@Site :
#@File : send-ding.py
#@Software: PyCharm

import requests
import json

def dingmessage(msg):
    webhook = "https://oapi.dingtalk.com/robot/send?access_token=ccb0598d0c9d5781717b7b51d4ab3ac082486e24aea3fca4df4076e6b31940ca"
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    #text文本格式
    # message = {
    #     "msgtype": "text",
    #     "at": {
    #         "atMobiles": ["13810697234"],
    #         "isAtAll": False
    #     },
    #     "text": {
    #         "content": "test" #发送的内容
    #     }
    # }
    # markdown文本格式
    message = {
        "msgtype": "markdown",
        "markdown": {
            "title": "打包地址:",
            "text": "打包地址："+msg
        },
        "at": {
            # @指定报警人
            "atMobiles": ["13810697234"],
            "isAtAll": True
        }
    }
    message_json = json.dumps(message)
    print(message_json)
    info = requests.post(url=webhook,data=message_json,headers=header)
    print(info.text)

if __name__=="__main__":
    dingmessage("testt")