# -*- coding:utf-8 -*-

import os
import numpy as np
from PIL import Image

#将警告变为异常可以捕捉
import warnings
warnings.filterwarnings("error", category=UserWarning)
##由于网上爬虫爬的图，有好多是错误的会有EXIF警告，需要处理，
#还有一些图像打不开因此需要处理

path = '../datasets'
filelists = os.listdir(path)


try:
    img_path = os.path.join(path,_file)
    img = Image.open(img_path)
except:
    os.remove(img_path)
    os.remove(os.path.join(path, _file.split('.')[0] + '.txt'))
    print(img_path)
