#!/usr/bin/env python3
#coding: utf8

# Pixels: (512*512)*294*12 = 924844032

import os

from PIL import Image

BOX_WIDTH  = 512
BOX_HEIGHT = 512
BOX_SIZE   = BOX_WIDTH*BOX_HEIGHT

def read_box(x, y):
    name = "data/l5_%d_%d.jpg" % (y, x)
    im = Image.open(name)
    pixels = tuple(im.getdata())
    assert(len(pixels) == BOX_WIDTH*BOX_HEIGHT)
    return pixels

def put_box(x, y, im):
    pixels = read_box(x+1, y+1)
    sx = BOX_WIDTH * x
    sy = BOX_HEIGHT * y
    for col in range(511):
        for row in range(511):
            im.putpixel((sx+col, sy+row), pixels[col*row])

def main():
    if not os.path.exists('result'):
        os.mkdir('result')
    
    im = Image.new('RGB', (512*294, 512*12))
    for x in range(293):
        for y in range(11):
            print("Process  ./data/l5_%03d_%03d.jpg  ZONE: SX: %06d EX: %06d SY: %06d EY: %06d  %sd pixels" \
                % (y+1, x+1, x*512, x*512+512, y*512, y*512+512, BOX_SIZE) )
            put_box(x, y, im)
    im.show()
    im.save("result/output.jpg")

if __name__ == '__main__':
    main()