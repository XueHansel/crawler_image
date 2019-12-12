# -*- coding:utf-8 -*-

import os
import numpy as np
from PIL import Image

# Change the warning to Error, so that we could use try...except... to capture the warning
import warnings
warnings.filterwarnings("error", category=UserWarning)

# 1、Using the images downloaded from internet maybe get some EXIF warning, so we must delete these pictures.
# 2、some pictures is damaged, so we alseo need to delete these images.

path = '../datasets'
filelists = os.listdir(path)


try:
    img_path = os.path.join(path,_file)
    img = Image.open(img_path)
except:
    os.remove(img_path)
    print(img_path)
