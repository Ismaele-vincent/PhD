#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 15:17:11 2024

@author: aaa
"""

import cv2
import os

image_folder = "/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Images 1 column/Animation"
from PIL import Image
def make_gif():
    frames = [Image.open("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Images 1 column/Animation/chi"+str(j)+".png") for j in range(22)]
    frame_one = frames[0]
    frame_one.save("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Images 1 column/fit.gif", format="GIF", append_images=frames,
                save_all=True, duration=300, loop=0)
    
if __name__ == "__main__":
    make_gif()
