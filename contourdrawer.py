import json
import numpy as np
import cv2
import os
import argparse
import random

def randomcolors(cnt):
    '''
    产生一组随机颜色
    
    输入：
    cnt：int，需要的颜色数量
    
    输出：
    colors：list，每个元素是一个三元组，表示一种颜色
    '''
    random.seed(0)
    colors = []
    for i in range(cnt):
        c = [144, 255, random.randint(0, 255)]
        random.shuffle(c)
        colors.append(tuple(c))
    return colors


def draw(fin, fout, seg, cat, showimg):
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
    if not(os.path.exists(fin)):
        raise FileNotFoundError(f'The file {fin} does not exist!')
    
    colors = randomcolors(max(cat))
    image = cv2.imread(fin)    
    for i in range(len(seg)):
        cv2.drawContours(image, [seg[i]], -1, colors[cat[i] - 1], 2)
        cv2.putText(image, str(cat[i]), (seg[i][0][0], seg[i][0][1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors[cat[i] - 1], 2)
    if showimg:
        cv2.imshow('image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    cv2.imwrite(fout, image)

def drawcontour(fjs, finput, foutput, showimg):
    '''
    从json文件中读取数据，并将数据传入draw函数进行绘制
    
    输入：
    fjs：str，json文件路径
    finput：str，输入图片所在文件夹的路径
    foutput：str，输出图片所在文件夹的路径
    showimg：bool，是否在运行时展示绘制结果
    
    输出：无
    '''
    with open(fjs, 'r', encoding = 'utf-8') as file:  
        json_str = file.read()
    js = json.loads(json_str)
    img = js['images']
    anno = js['annotations']
    
    if (len(img) == 0 or len(anno) == 0):
        raise ValueError('The .json file is empty!')
    
    imgname = {}
    for i in img:
        imgname[i['id']] = i['file_name']
    
    id0 = anno[0]['image_id']
    seg = []
    cat = []
    for i in range(len(anno)):
        if (len(anno[i]['segmentation']) == 4):
            temp = [anno[i]['segmentation'][0], anno[i]['segmentation'][1],
                    anno[i]['segmentation'][0], anno[i]['segmentation'][3],
                    anno[i]['segmentation'][2], anno[i]['segmentation'][3],
                    anno[i]['segmentation'][2], anno[i]['segmentation'][1]]
            anno[i]['segmentation'] = temp
        anno[i]['segmentation'] = list(map(int, anno[i]['segmentation']))
        seg.append(np.array(anno[i]['segmentation']).reshape(4, 2))
        cat.append(anno[i]['category_id'])
        if (i == len(anno) - 1 or anno[i + 1]['image_id'] != id0):
            try:
                draw(os.path.join(finput, imgname[id0]), os.path.join(foutput, imgname[id0]), seg, cat, showimg) 
            except KeyError:
                print(f'The .json file does not contain the file_name of image_id {id0}!')
            if (i < len(anno) - 1):
                id0 = anno[i + 1]['image_id']
                seg = []
                cat = []
        
def run():
    '''
    设置命令行参数并运行
    
    输入：无
    
    输出：无
    '''
    parser = argparse.ArgumentParser(description = 'Expected 0 to 4 arguments.')
    parser.add_argument('-j', '--fjs', type=str, default='result.json')
    parser.add_argument('-i', '--finput', type=str, default=os.path.join(os.getcwd(), 'image'))
    parser.add_argument('-o', '--foutput', type=str, default=os.path.join(os.getcwd(), 'result'))
    parser.add_argument('-s', '--showimg', action='store_true', default=False)
    args = parser.parse_args()
    fjs = args.fjs
    finput = args.finput
    foutput = args.foutput
    showimg = args.showimg
    
    if not(os.path.exists(fjs)):
        raise FileNotFoundError(f'The file {fjs} does not exist!')
    if not(os.path.exists(finput)):
        raise FileNotFoundError(f'The file {finput} does not exist!')
    if not(os.path.exists(foutput)):
        os.mkdir(foutput)
    drawcontour(fjs, finput, foutput, showimg)

if __name__ == '__main__':
    run()