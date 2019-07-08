基于图像的水表读数读取方法  
==================

##环境依赖  
python opencv version:3.4.4

python 3.7.3

##部署步骤  
1.添加python opencv环境:
    pip install opencv-python

##目录结构描述  
├── Readme.md                   // readme概述  
├── main.py                     // 算法主要部分  

##算法概述  
算法由以下几个步骤组成：  
├── 图像预处理  
├── 圆检测  
├── 指针提取  
├── 指针角度计算  
└── 示数计算与校正  
1.输入一张水表图像，经过算法处理后，可以算得水表下方指针的读数。  
2.目前可以支持读取三个小表盘以上的水表，读取的表盘倍数需要自左向右依次变大。  
3.指针颜色必须为红色  
4.水表图像必须摆正  
5.图像需要为正方形，且分辨率大于800*800