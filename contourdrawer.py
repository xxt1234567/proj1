import json
import numpy as np
import cv2
import os
import argparse
from random import *

def draw(fin, fout, seg, cat, showimg=False):
    '''
    绘制框体
    
    输入：
    fin：str，输入图片路径
    fout：str，输出图片路径
    seg：list，每个元素是一个4 * 2的numpy array，记录一个框体四个顶点的坐标
    cat：list，框体的类别
    showimg：bool，是否在运行时展示绘制结果
    
    输出：无
    '''
    '''
    cnum = max(cat)
    seed(0)
    colors = []
    for i in range(cnum):
        rgb = (randint(0, 255), randint(0, 255), randint(0, 255))
        colors.append(rgb)
    '''
    colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
    image = cv2.imread(fin)    
    for i in range(len(seg)):
        cv2.drawContours(image, [seg[i]], -1, colors[cat[i] - 1], 1)
        cv2.putText(image, str(cat[i]), (seg[i][0][0], seg[i][0][1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors[cat[i] - 1], 1)
    if showimg:
        cv2.imshow('image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    cv2.imwrite(fout, image)

def drawcontour(fjs, finput, foutput):
    '''
    从json文件中读取数据，并将数据传入draw函数进行绘制
    
    输入：
    fjs：str，json文件路径
    finput：str，输入图片所在文件夹的路径
    foutput：str，输出图片所在文件夹的路径
    
    输出：无
    '''
    with open(fjs, 'r', encoding = 'utf-8') as file:  
        json_str = file.read()
    js = json.loads(json_str)
    img = js['images']
    anno = js['annotations']
    imgname = {}
    for i in img:
        imgname[i['id']] = i['file_name']
    id0 = None
    seg = []
    cat = []
    for i in anno:
        if not(i['image_id'] == id0):
            if not(id0 is None):
                draw(os.path.join(finput, imgname[id0]), os.path.join(foutput, imgname[id0]), seg, cat)
            id0 = i['image_id']
            seg = []
            cat = []
        if (len(i['segmentation']) == 4):
            temp = [i['segmentation'][0], i['segmentation'][1],
                    i['segmentation'][0], i['segmentation'][3],
                    i['segmentation'][2], i['segmentation'][3],
                    i['segmentation'][2], i['segmentation'][1]]
            i['segmentation'] = temp
        i['segmentation'] = list(map(int, i['segmentation']))
        seg.append(np.array(i['segmentation']).reshape(4, 2))
        cat.append(i['category_id'])
    if not(id0 is None):
        draw(os.path.join(finput, imgname[id0]), os.path.join(foutput, imgname[id0]), seg, cat)    
        
def run():
    '''
    设置命令行参数并运行
    
    输入：无
    
    输出：无
    '''
    parser = argparse.ArgumentParser(description = 'Expected 0 to 3 arguments')
    parser.add_argument('-j', '--fjs', type=str, default='result.json')
    parser.add_argument('-i', '--finput', type=str, default=os.path.join(os.getcwd(), 'image'))
    parser.add_argument('-o', '--foutput', type=str, default=os.path.join(os.getcwd(), 'result'))
    args = parser.parse_args()
    fjs = args.fjs
    finput = args.finput
    foutput = args.foutput
    if not(os.path.exists(foutput)):
        os.mkdir(foutput)
    drawcontour(fjs, finput, foutput)

if __name__ == '__main__':
    run()