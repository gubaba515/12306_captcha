import argparse

import cv2
import numpy as np
import random
from PIL import Image,ImageDraw,ImageFont
import os
import uuid
if __name__ == '__main__':

    parse = argparse.ArgumentParser()
    parse.add_argument('--font_path', required=True, help='the font location')
    parse.add_argument('--font_size', required=True,type=int, help='the font size')
    parse.add_argument('--word_document', required=True, help='the document contain lines of words')
    parse.add_argument('--image_store_path', required=True, help='where do you want to save the images')
    parse.add_argument('--spare_height', required=False,default=10,type=int, help='make the image much more beautiful')
    parse.add_argument('--file_list_document', required=True,
                       help="the csv document contain lines of the picture absolute path and the correspond text")

    opt = parse.parse_args()
    bgcolor = (0,0,0)
    fontcolor = (255,255,255)

    font = ImageFont.truetype(opt.font_path, opt.font_size)
    tps_width = opt.font_size
    scale_height = opt.spare_height
    with open (opt.word_document) as to_read,open(opt.file_list_document,'w') as to_write:
        for line in to_read:
            line = line.strip()
            font_width, font_height = font.getsize(line)
            image = Image.new('RGBA', (font_width, font_height+opt.spare_height*2), bgcolor)
            draw = ImageDraw.Draw(image)
            draw.text((0, opt.spare_height), line,font=font, fill=fontcolor)

            img = np.array(image)
            tps = cv2.createThinPlateSplineShapeTransformer()
            # tps.setRegularizationParameter(0.3)
            height,width,channel = img.shape
            pt_1 = [[x,opt.spare_height] for x in range(0,width,tps_width)] +\
                   [[x,height-opt.spare_height] for x in range(0,width,tps_width)]
            pt_2 = [[pt[0],random.randint(-scale_height,scale_height)+pt[1]] for pt in pt_1]
            pt_size = len(pt_1)
            matches = [cv2.DMatch(i,i,0) for i in range(pt_size)]
            M = tps.estimateTransformation(
                np.array(pt_1).reshape((1,pt_size,2)),
                np.array(pt_2).reshape((1,pt_size,2)),
                matches
            )
            res = tps.warpImage(img,M)
            res = 255 - res
            img_filename = os.path.join(opt.image_store_path,'%s.jpg'%uuid.uuid4())
            cv2.imwrite(img_filename,res)
            to_write.write('%s,%s\n'%(img_filename,line))