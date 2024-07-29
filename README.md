# 标注框体绘制器

## 简介

一个python脚本，通过读取存放在json文件中的标注信息，在图片中画出标注框体和类别并另存。

## 所需环境和第三方库

* python 3.9.13
* numpy 1.23.5
* opencv-python 4.9.0.80

## 运行方式

在Windows命令行中运行。注意先使用``cd``命令切换到包含Python脚本的目录。

可以在命令行中输入``-j``，``-i``，``-o``三个参数来分别指定``.json``文件、输入图片所在的文件夹、输出图片要存放到的文件夹的目录。

不输入参数时，它们的默认值分别为``result.json``，``image``和``result``。

## 运行示例

```
python contourdrawer.py
```
读取与``contourdrawer.py``脚本在同一目录下的``result.json``文件和``image``文件夹中的图片，绘制框体后保存在同一目录下的``result``文件夹中。


```
python contourdrawer.py -j D:\test.json
```
读取``D:\test.json``文件，以及和``contourdrawer.py``脚本在同一目录下的``image``文件夹中的图片，绘制框体后保存在和``contourdrawer.py``脚本同一目录下的``result``文件夹中。


```
python contourdrawer.py -j D:\test.json -i D:\input -o D:\output
```
读取``D:\test.json``文件以及``D:\input``文件夹中的图片，绘制框体后保存到``D:\output``文件夹中。

###### 若输出文件夹不存在，脚本会自动在指定目录下创建文件夹。参数数量多于3个，格式不正确或指定的输入文件目录不存在将会报错。