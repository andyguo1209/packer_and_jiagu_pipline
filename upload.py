#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@Time : 2020/8/20 下午10:17
#@Author : guozhenhua
#@Site : 
#@File : upload.py
#@Software: PyCharm

import os
import time
import sys
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


def uploadFile(url,api_key,description,workspace):

    # #账号配置信息
    # url = "https://www.pgyer.com/apiv2/app/upload"
    # api_key="a2f9d12e3eaae51a435a665923377cec"


    #获取时间戳
    currentTime= (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))



    apkPath =workspace+"/app/build/outputs/apk/debug/app-debug.apk"

    apkfile = {"file":open(apkPath,"rb")}
    headers = {"enctype":"multipart/form-data"}
    payload= {
        "buildInstallType":2,
        "_api_key":api_key,
        "installType":1,
        "buildPassword":"hixiaohe",
        "buildUpdateDescription":"android自动化打包"
    }

    r = requests.post(url,data= payload,headers=headers,files = apkfile)
    jsonResult = r.json()
    print(jsonResult)

    #保存二维码至本地
    appQRCodeURL = jsonResult["data"]["appQRCodeURL"]
    print("appQRCodeURL: %s "%appQRCodeURL)
    response = requests.get(appQRCodeURL)
    imgp = "/opt/image"
    qr_image_file_path = os.path.join(imgp,"QRCode.png")
    print(qr_image_file_path)

    with open(qr_image_file_path,"wb") as f:
        f.write(response.content)

    return jsonResult


if __name__ == '__main__':

    url = "https://www.pgyer.com/apiv2/app/upload"
    api_key="a2f9d12e3eaae51a435a665923377cec"

    # 从jenkins获取描述
    description = sys.argv[1]

    # 获取jenkins的目录地址
    workspace = sys.argv[2]

    jsonResult=uploadFile(url,api_key,description,workspace)

    dingmessage(jsonResult)

