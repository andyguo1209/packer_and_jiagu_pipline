#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@Time : 2020/8/22 下午2:31
#@Author : guozhenhua
#@Site : 
#@File : test.py
#@Software: PyCharm



import subprocess


def get_upload_file_name(file_path):
    get_file_name_cmd = "ls " + file_path + " |grep debug-v2.0.8.0803-aiyouguanwang"

    sub = subprocess.Popen(get_file_name_cmd, shell=True,
                           stdout=subprocess.PIPE)
    sub.wait()
    file_name=sub.stdout.read().decode()

    return file_name

file_path="/Users/guozhenhua/Downloads"

print(get_upload_file_name(file_path))




