#!/usr/bin/env python3
#coding: utf8

import os
import time

from PIL import Image

# width  = 512 * 294
# height = 512 * 12
# pixels = width * height
# bytes  = pixels * 3
# bits   = bytes * 8

print(" Width: 512 * 294 = 150528")
print("Height: 512 *  12 = 6144")
print("Pxiels: 150528 * 6144 = 924_844_032")
print(" Bytes: 924_844_032 * 3 = 2_774_532_096      ( 2_774_532_096/1024/1024 = 2646 MB )")
print("  Bits: 2_774_532_096 * 8 = 22_196_256_768")

#  Width: 512 * 294 = 150528
# Height: 512 *  12 = 6144
# Pxiels: 150528 * 6144 = 924_844_032
#  Bytes: 924_844_032 * 3 = 2_774_532_096    
#   Bits: 2_774_532_096 * 8 = 22_196_256_768

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
    
    btime = time.time()

    im = Image.new('RGB', (512*294, 512*12))
    for x in range(293):
        for y in range(11):
            print("Process  ./data/l5_%03d_%03d.jpg  ZONE: SX: %06d EX: %06d SY: %06d EY: %06d  %s pixels" \
                % (y+1, x+1, x*512, x*512+512, y*512, y*512+512, BOX_SIZE) )
            put_box(x, y, im)

    etime = time.time()

    print("\n\n[DONE] Duration: %fs" % etime - btime)

    im.show()
    im.save("result/output.jpg")

if __name__ == '__main__':
    main()