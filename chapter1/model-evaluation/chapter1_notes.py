#!-*- coding: utf-8 -*-
# !/usr/bin/python3
'''

#Copyright: 
#File Name:     .py
#Project:  
#Software: 
#Version:       Initial Draft
#Author:         
#Created:       2022-02-12
#Last Modified: 2022-02-12 23:23:18
#Description:   描述主要实现的功能
#Function List: xxx
'''

# 当前工作路径 文件路径 绝对路径 辨析
import os
import yaml
print('os.path.dirname(__file__): \n', os.path.dirname(__file__))

print('os.getcwd(): \n', os.getcwd())

print('os.path.abspath(__file__): \n', os.path.abspath(__file__))

gtFolder = 'chapter1/model-evaluation/data/groundtruths'

files = os.listdir(gtFolder)
print(files)

conf_path = './chapter1/model-evaluation/conf/conf.yaml'

with open(conf_path, 'r', encoding='utf-8') as f:
    data=f.read()
# 使用yaml.load加载YAML文件，然后以python的数据格式方式进行展示，从而方便使用python对YAML中的数据进行读取操作
cfg = yaml.load(data,Loader=yaml.FullLoader)

print(cfg["iouThreshold"],cfg["colors"][0])