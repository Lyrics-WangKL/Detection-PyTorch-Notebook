import os
from Evaluator import *
import pdb

def getGTBoxes(cfg, GTFolder):
    '''获取GT 标签数据
        
        从GTFolder目录下依次读取标签信息，并解析

        parameters:
            cfg: 本函数暂未用到
            GTFloder: gt 标签存放路径
        return:
            gt_boxes: 标签类别，数量和对应的box坐标
            classes: 类别列表
            num_pos: 类别出现的次数
    '''
    # 返回指定的文件夹包含的文件或文件夹的名字的列表。
    files = os.listdir(GTFolder)
    files.sort()
    
    # 初始化类别标签，数组。用于存放 GT标签
    classes = []
    # 位置的个数，用字典表示，key值为类别
    num_pos = {}
    # 真值的box位置，用字典表示，嵌套字典
    # git_boxes{class{'1':...}}
    gt_boxes = {}
    for f in files:
        # 路径拼接，获取files列表中的每一个文件
        # 每个文件代表了一张图片中的 GT 标签
        nameOfImage = f.replace(".txt", "")
        # 直接使用open()打开文件，需要记住使用 close()关闭，释放内存
        fh1 = open(os.path.join(GTFolder, f), "r")
        
        for line in fh1:
            # fh1 文件中每一行表示一个类别标签和box的坐标
            # 去掉每一行的换行符
            line = line.replace("\n", "")
            # TODO 2022/02/17 这段替换空格目的是什么？
            # 文件最后一行为空行，识别到空行之后，跳过后续步骤
            if line.replace(' ', '') == '':
                continue
            splitLine = line.split(" ")

            cls = (splitLine[0])  # class
            left = float(splitLine[1])
            top = float(splitLine[2])
            right = float(splitLine[3])
            bottom = float(splitLine[4]) 
            # TODO 2022/02/17 one_box 最后1个值 0表示什么？ 
            one_box = [left, top, right, bottom, 0]
              
            if cls not in classes:
                # 如果类别第1次出现，那么创建该类别的键值
                classes.append(cls)
                gt_boxes[cls] = {}
                num_pos[cls] = 0
            # TODO 2022/02/18 num_pos只是标记了类别cls出现的次数，
            # 那么如何知道这个类别在某张图片(nameOfImage)中出现的次数？
            num_pos[cls] += 1

            if nameOfImage not in gt_boxes[cls]:
                # 如果图片名称第一次出现，那么创建该图片名的键值
                gt_boxes[cls][nameOfImage] = []
            # 最后获得的是git_box 某类别cls在nameOfImage图片的box框
            gt_boxes[cls][nameOfImage].append(one_box)  
        # 关闭文件 
        fh1.close()
    return gt_boxes, classes, num_pos

def getDetBoxes(cfg, DetFolder):

    files = os.listdir(DetFolder)
    files.sort()

    det_boxes = {}
    for f in files:
        nameOfImage = f.replace(".txt", "")
        fh1 = open(os.path.join(DetFolder, f), "r")

        for line in fh1:
            line = line.replace("\n", "")
            if line.replace(' ', '') == '':
                continue
            splitLine = line.split(" ")

            cls = (splitLine[0])  # class
            left = float(splitLine[1])
            top = float(splitLine[2])
            right = float(splitLine[3])
            bottom = float(splitLine[4])
            score = float(splitLine[5])
            one_box = [left, top, right, bottom, score, nameOfImage]

            if cls not in det_boxes:
                det_boxes[cls]=[]
            det_boxes[cls].append(one_box)

        fh1.close()
    return det_boxes

def detections(cfg,
               gtFolder,
               detFolder,
               savePath,
               show_process=True):
    

    gt_boxes, classes, num_pos = getGTBoxes(cfg, gtFolder)
    det_boxes = getDetBoxes(cfg, detFolder)
    
    evaluator = Evaluator()

    return evaluator.GetPascalVOCMetrics(cfg, classes, gt_boxes, num_pos, det_boxes)

def plot_save_result(cfg, results, classes, savePath):
    
    
    plt.rcParams['savefig.dpi'] = 80
    plt.rcParams['figure.dpi'] = 130

    acc_AP = 0
    validClasses = 0
    fig_index = 0

    for cls_index, result in enumerate(results):
        if result is None:
            raise IOError('Error: Class %d could not be found.' % classId)

        cls = result['class']
        precision = result['precision']
        recall = result['recall']
        average_precision = result['AP']
        acc_AP = acc_AP + average_precision
        mpre = result['interpolated precision']
        mrec = result['interpolated recall']
        npos = result['total positives']
        total_tp = result['total TP']
        total_fp = result['total FP']

        fig_index+=1
        plt.figure(fig_index)
        plt.plot(recall, precision, cfg['colors'][cls_index], label='Precision')
        plt.xlabel('recall')
        plt.ylabel('precision')
        ap_str = "{0:.2f}%".format(average_precision * 100)
        plt.title('Precision x Recall curve \nClass: %s, AP: %s' % (str(cls), ap_str))
        plt.legend(shadow=True)
        plt.grid()
        plt.savefig(os.path.join(savePath, cls + '.png'))
        plt.show()
        plt.pause(0.05)


    mAP = acc_AP / fig_index
    mAP_str = "{0:.2f}%".format(mAP * 100)
    print('mAP: %s' % mAP_str)
    
