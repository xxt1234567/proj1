# 标注框体绘制器

## 简介

一个python脚本，通过读取存放在json文件中的标注信息，在图片中画出标注框体和类别并另存。

## 所需python库

* numpy
* json
* cv2
* sys
* os

## 运行方式及示例

在Windows命令行中运行。注意先使用``cd``命令切换到包含Python脚本的目录。

###### 0个参数：

```
python contourdrawer.py
```
读取与``contourdrawer.py``脚本在同一目录下的``result.json``文件和``image``文件夹中的图片，绘制框体后保存在同一目录下的``result``文件夹中。

###### 1个参数，指定.json文件目录：

```
python contourdrawer.py D:\test.json
```
读取指定目录下的``.json``文件，以及和``contourdrawer.py``脚本在同一目录下的``image``文件夹中的图片，绘制框体后保存在和``contourdrawer.py``脚本同一目录下的``result``文件夹中。

###### 3个参数，指定.json文件和输入输出图片文件夹目录：

```
python contourdrawer.py D:\test.json D:\input D:\output
```
读取指定目录下的``.json``文件和输入文件夹中的图片，绘制框体后保存指定目录下的输出文件夹中。

###### 参数数量不正确或指定的输入文件目录不存在将会报错。