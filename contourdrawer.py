import json
import numpy as np
import cv2
import os
import argparse

def readjs(fjs):
    with open(fjs,'r',encoding='utf-8') as file:  
        json_str=file.read()
    js=json.loads(json_str)
    info=js['images']
    rects=js['annotations']
    for i in rects:
        for j in range(len(i['segmentation'])):
            i['segmentation'][j]=int(i['segmentation'][j])
    return info,rects

def getcontourdata(info,rects):
    data={}
    for i in info:
        data[i['id']]={}
        data[i['id']]['file_name']=i['file_name']
        data[i['id']]['segmentation']=[]
        data[i['id']]['category_id']=[]
    for i in rects:
        data[i['image_id']]['segmentation'].append(np.array(i['segmentation']).reshape(4,2))
        data[i['image_id']]['category_id'].append(i['category_id'])
    return data

def drawcontour(data,finput,foutput,showimg=False):
    colors=[(0,0,0),(255,0,0),(0,255,0),(0,0,255)]
    for i in data:
        image=cv2.imread(os.path.join(finput,data[i]['file_name']))
        for j in range(len(data[i]['segmentation'])):
            cv2.drawContours(image,[data[i]['segmentation'][j]],-1,colors[data[i]['category_id'][j]-1],1)
            cv2.putText(image,str(data[i]['category_id'][j]),(data[i]['segmentation'][j][0][0],data[i]['segmentation'][j][0][1]),cv2.FONT_HERSHEY_SIMPLEX,0.5,colors[data[i]['category_id'][j]-1],1)
        if showimg:
            cv2.imshow('image',image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        cv2.imwrite(os.path.join(foutput,data[i]['file_name']),image)

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='Expected 0 to 3 arguments')
    parser.add_argument('-j','--fjs',type=str,default='result.json')
    parser.add_argument('-i','--finput',type=str,default=os.path.join(os.getcwd(),'image'))
    parser.add_argument('-o','--foutput',type=str,default=os.path.join(os.getcwd(),'result'))
    args=parser.parse_args()
    fjs=args.fjs
    finput=args.finput
    foutput=args.foutput
    if not(os.path.exists(foutput)):
        os.mkdir(foutput)
        
    info,rects=readjs(fjs)
    data=getcontourdata(info,rects)
    drawcontour(data,finput,foutput)