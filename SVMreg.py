#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, Image,ImageEnhance,ImageFilter
#os.chdir('F:\Downloads\libsvm-3.18\python')
from svmutil import *
# this function is the same as which in prepareSVMdata.py
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
#this function divide the image to single character image ,but we use other format to save the data
#because we don't know the single character, it is the data to be recognized
def division(img):        #图像的分割，就是验证码按字符分割出来
    #modsamples =['2','4','6','8','b','d','f','h','j','l','n','p','r','t','v','x','z']
    #nume=imgfile[0:4]
    font=[]
    tempInstance=''
    for i in range(4):
        x=7+i*(18+6)        #该函数中的像素值都需要自己进行微调
        y=1
        temp = img.crop((x,y,x+18,y+26))
        #temp.save("./temp/%d.tif" % nume[i])
        
        k=1
        pixdata = temp.load()
        tempInstance=[]
        for y in xrange(temp.size[1]):
            for x in xrange(temp.size[0]):
                if pixdata[x, y][0] < 255:
                    tempInstance.append(0)
                else:
                    tempInstance.append(1)
                k=k+1
        #tempInstance+=('\n')
        font.append(tempInstance)
        
    return font
if __name__ == '__main__':
    picturedir="./ImageTotal/"
    #the set of characters in the captcha,and the first class represent '0', the sencond class represent '1',and so on
    modsamples =['0','1','2','3','4','5','6','7','8','9']
    #load the model we trained before
    m = svm_load_model('trainingSamples.model')
    
    total =0
   
    for imgfile in os.listdir(picturedir):
        resultName=''
        if imgfile.endswith(".tif"):
            total += 1
            
            img=binary(picturedir+imgfile)
            img = img.filter(ImageFilter.MedianFilter())
            instances=division(img)
            for instance in instances:
		x0,max_idx = gen_svm_nodearray(instance)
        	label = libsvm.svm_predict(m, x0)
        	print label
        	resultName+=modsamples[int(label)]
            img.save("./recognizedImage/%s.tif" % resultName)
    
            
            #enhancer = ImageEnhance.Contrast(img)
            #img = enhancer.enhance(2)
    
