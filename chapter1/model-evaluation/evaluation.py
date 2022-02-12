import os
import sys
import yaml

# sys.path.insert(0, os.path.join(os.getcwd(), 'lib'))
# os.getcwd() 获取的是当前工作路径 current work directory，因此，
# 当前程序执行时候，获取到的是工作路径C:\Users\super\Documents\GitHub\Detection-PyTorch-Notebook
# 所以 os.getcwd()要慎用！！
# 保险的做法是获取绝对路径
# os.path.abspath(__file__)
print(os.getcwd())
# 拼接得到的是错误的路径
print(os.path.join(os.getcwd(), 'chapter1\model-evaluation\lib'))
# 正确做法
print(os.path.abspath(__file__))
print(os.path.abspath(__file__), 'lib')

sys.path.insert(0, os.path.join(os.getcwd(), 'chapter1\model-evaluation\lib'))
from detection import detections, plot_save_result

conf_path = './chapter1/model-evaluation/conf/conf.yaml'

with open(conf_path, 'r', encoding='utf-8') as f:
    data=f.read()
# 使用yaml.load加载YAML文件，然后以python的数据格式方式进行展示，从而方便使用python对YAML中的数据进行读取操作
cfg = yaml.load(data,Loader=yaml.FullLoader)

gtFolder = 'chapter1/model-evaluation/data/groundtruths'
detFolder = 'chapter1/model-evaluation/data/detections'
savePath = 'chapter1/model-evaluation/data/results'

results, classes = detections(cfg, gtFolder, detFolder, savePath)
plot_save_result(cfg, results, classes, savePath)
