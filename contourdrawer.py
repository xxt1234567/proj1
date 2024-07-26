import json
import numpy as np
import cv2
import sys
import os

if (len(sys.argv)==1):
    fjs='result.json'
    finput='.\image\\'
    foutput='.\\result\\'
elif (len(sys.argv)==2):
    fjs=sys.argv[1]
    finput='.\image\\'
    foutput='.\\result\\'
elif (len(sys.argv)==4):
    fjs=sys.argv[1]
    finput=sys.argv[2]+'\\'
    foutput=sys.argv[3]+'\\'
else:
    assert 0,"Expected 0, 1, or 3 arguments"

if not(os.path.exists(foutput)):
    os.mkdir(foutput)
    
colors=[(0,0,0),(255,0,0),(0,255,0),(0,0,255)]

with open(fjs,'r',encoding='utf-8') as file:  
    json_str=file.read()
js=json.loads(json_str)
info=js['images']
rects=js['annotations']
for i in rects:
    for j in range(len(i['segmentation'])):
        i['segmentation'][j]=int(i['segmentation'][j])
data={}
for i in info:
    data[i['id']]={}
    data[i['id']]['file_name']=i['file_name']
    data[i['id']]['segmentation']=[]
    data[i['id']]['category_id']=[]
for i in rects:
    data[i['image_id']]['segmentation'].append(np.array(i['segmentation']).reshape(4,2))
    data[i['image_id']]['category_id'].append(i['category_id'])
    
for i in data:
    image=cv2.imread(finput+data[i]['file_name'])
    im2=image
    for j in range(len(data[i]['segmentation'])):
        cv2.drawContours(im2,[data[i]['segmentation'][j]],-1,colors[data[i]['category_id'][j]-1],1)
        #cv2.putText(im2,str(data[i]['category_id'][j]),((data[i]['segmentation'][j][0][0]+data[i]['segmentation'][j][1][0]+data[i]['segmentation'][j][2][0]+data[i]['segmentation'][j][3][0])//4,(data[i]['segmentation'][j][0][1]+data[i]['segmentation'][j][1][1]+data[i]['segmentation'][j][2][1]+data[i]['segmentation'][j][3][1])//4),cv2.FONT_HERSHEY_SIMPLEX,0.5,colors[data[i]['category_id'][j]-1],1)
        cv2.putText(im2,str(data[i]['category_id'][j]),(data[i]['segmentation'][j][0][0],data[i]['segmentation'][j][0][1]),cv2.FONT_HERSHEY_SIMPLEX,0.5,colors[data[i]['category_id'][j]-1],1)
    #cv2.imshow('1',im2)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    cv2.imwrite(foutput+data[i]['file_name'],im2)