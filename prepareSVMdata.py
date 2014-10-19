#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os,Image,ImageEnhance,ImageFilter
#binarize the image
def binary(f):                #图像的二值化处理
    print f
    img = Image.open(f)
    #img = img.convert('1')
    img = img.convert("RGBA")  #参考文章中无该行，无该行，我这里会报错
    
    pixdata = img.load()
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][0] < 90:
                pixdata[x, y] = (0, 0, 0, 255)
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][1] < 136:
                pixdata[x, y] = (0, 0, 0, 255)
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][2] > 0:
                pixdata[x, y] = (255, 255, 255, 255)
    return img
nume = 0
#divide the image to single character
def division(img,imgefile):        #图像的分割，就是验证码按字符分割出来
    # the first class represent '0', the sencond class represent '1',and so on 
    modsamples =['0','1','2','3','4','5','6','7','8','9']
    nume=imgfile[0:4]
    font=''
    for i in range(4):
        """
        "7" 验证码离图像左边框距离（单位：像素）
        “18”像素宽度        
        """
        #you need change the digital to crop out the right and whole character
	x=7+i*(18+6)        #该函数中的像素值都需要自己进行微调
        y=1
        temp = img.crop((x,y,x+18,y+26))
	#if you need ,you can save the image divided to check whether it is correct
        #temp.save("./temp/%s.tif" % (nume[i]+str(total)))
        font+= str(modsamples.index(nume[i]))+' '
        k=1
        pixdata = temp.load()
        for y in xrange(temp.size[1]):
            for x in xrange(temp.size[0]):
                if pixdata[x, y][0] < 255:
                    font+=(str(k)+':'+'0 ')
                else:
                    font+=(str(k)+':'+'1 ')
                k=k+1
        font+=('\n')
        
    return font
total =0
if __name__ == '__main__':
    picturedir="./namedImage/"
   
    fileHandle=open('trainingSamples','a')
    for imgfile in os.listdir(picturedir):
        if imgfile.endswith(".tif"):
            total += 1
            
            img=binary(picturedir+imgfile)
            img = img.filter(ImageFilter.MedianFilter())
            #img.save("./temp/%s.tif" % imgfile[0:4])
            trainingSample=division(img,imgfile)
            fileHandle.write(trainingSample)
    fileHandle.close()
            
            #enhancer = ImageEnhance.Contrast(img)
            #img = enhancer.enhance(2)
    
