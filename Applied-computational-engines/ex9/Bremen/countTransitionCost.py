#!/usr/bin/python2

import os
import sys
import math
import glob
from PIL import Image

for first in glob.glob("*.png"):
    for second in glob.glob("*.png"):
        if first!=second:
            inImage1 = Image.open(first)
            inImage2 = Image.open(second)

            # Left / right
            pal1 = inImage1.getpalette()
            pal2 = inImage2.getpalette()
            
            totalDiff = 0.0
            for y in range(0,inImage1.height):
                pix1 = inImage1.getpixel((inImage1.width-1,y))
                pix2 = inImage2.getpixel((0,y))
                diffR = pal1[pix1*3] - pal2[pix2*3]
                diffG = pal1[pix1*3+1] - pal2[pix2*3+1]
                diffB = pal1[pix1*3+2] - pal2[pix2*3+2]
                totalDiff += math.sqrt(diffR*diffR+diffG*diffG+diffB*diffB)
            
            print int(totalDiff/1000.0),first,second,"LR"
            
            # Up / Down
            totalDiff = 0.0
            for x in range(0,inImage1.width):
                pix1 = inImage1.getpixel((x,inImage1.height-1))
                pix2 = inImage2.getpixel((x,0))
                diffR = pal1[pix1*3] - pal2[pix2*3]
                diffG = pal1[pix1*3+1] - pal2[pix2*3+1]
                diffB = pal1[pix1*3+2] - pal2[pix2*3+2]
                totalDiff += math.sqrt(diffR*diffR+diffG*diffG+diffB*diffB)
            
            print int(totalDiff/1000.0),first,second,"UD"
            
            
