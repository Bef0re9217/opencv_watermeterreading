基于图像的水表读数读取方法  
Image-based water meter reading method
==================

##环境依赖  
Dependence
python opencv version:3.4.4

python 3.7.3

##部署步骤  
Deploy
1.添加python opencv环境:  
pip install opencv-python

##目录结构描述  
├── Readme.md                   // readme概述  
├── main.py                     // 算法主要部分  Main algorithm

##算法概述  
算法由以下几个步骤组成：  
This algorithm consists of the following steps:  
├── 图像预处理  imagine preprocessing  
├── 圆检测  circle detect  
├── 指针提取  pointer get  
├── 指针角度计算  pointer angel calculate  
└── 示数计算与校正  Reading correction  
1.输入一张水表图像，经过算法处理后，可以算得水表下方指针的读数。  
Input an watermeter image.This algorithm can calculate the reading of pointer
2.目前可以支持读取三个小表盘以上的水表，读取的表盘倍数需要自左向右依次变大。  
Support three dials.The read dial multiple needs to be larger from left to right.
3.指针颜色必须为红色  
Colour of pointer must be red
4.水表图像必须摆正  
Watermeter image must vertical
5.图像需要为正方形，且分辨率大于800*800
Resolution must bigger than 800*800

##Jul.10.2019 commit  
修复在ROI分辨率变化时可能会出现除数为0的bug
Fix divide 0 error while ROI change
