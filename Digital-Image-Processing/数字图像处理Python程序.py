#!/usr/bin/env python3
#-*- coding:utf-8 -*-

__author__="zhuxiang"

__version__=("0.0.0.0")

__purpose__=r'''数字图像处理作业'''

#以下类用于界面
from tkinter import*
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import *

#以下类用于图像处理
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter
import matplotlib.pyplot as plt
from pylab import *
#from numpy import *

#以下类用于文件操作
import os

#------函数开始-----
global filename

filename=None

#打开文件对话框并读取一个文件
def myopen():
    global filename
    filename=askopenfilename(defaultextension=".bmp",
        filetypes = [("JPG文件",".jpg"),("PNG文件",".png "),("BMP文件",".bmp"),("所有文件",".*")])


#转换成灰度图
def mygray():
    global filename
    img=Image.open(filename)
    gray=img.convert('L')
    plt.figure("灰度图")
    plt.imshow(gray,cmap='gray')
    plt.axis('off')
    plt.show()


#对图像进行反转
def myfanzhuan():
    global filename
    fanzhaun=Image.open(filename)#read image
    fanzhaun = array(fanzhaun.convert('L'))#transtor to gray
    # figure()
    fanzhuan=255-fanzhaun
    plt.imshow(fanzhuan)
    plt.axis('off')
    plt.show()
    
#直方图统计
def myzhifangtu():
    global filename
    zhifangtu1=Image.open(filename)#read image
    zhifangtugray = array(zhifangtu1.convert('L'))#transtor to gray
    figure()
    hist(zhifangtugray.flatten(),256)
    plt.show()

#缩略图   
    
def mysuo():
    global filename
    mys=Image.open(filename)
    mys.thumbnail((128,128))
    plt.imshow(mys)
    plt.show()

def myexit():
    exit()

def mybanben():
    showinfo(title="版本",message="第一版    version - 0.0.0.1")

def mybanquan():
    showinfo(title="版权",message="版权归制作者所有，未经同意可以复制！")

def myguanyu():
    showinfo(title="关于",message="朱想制作，品质保证")

def mychepai():
    if filename==None:
        showinfo(title="错误",message="没有选中图片！")
    else:
        im=Image.open(filename)
        r = im.convert('RGB')#转换成RGB模式
        a=[]
        for  i in range(r.size[0]):#把每个像素点的RGB值读取出来
            for j in range(r.size[1]):
                a.append(im.getpixel((i,j))) 
                
        blue = Image.new("RGB",(r.size[0],r.size[1])) 
        tushuju = 0 
        blueshuju=[]    
        huidu = 0
        haha=0
        #在蓝色色面 可以检测出蓝色的区域，但是对于靠近蓝色与车牌不清晰的图片效果会很差
        for  i in range(r.size[0]):
           for j in range(r.size[1]):
                if a[tushuju][0]<100 and a[tushuju][1]<100 and  a[tushuju][2]>150:
                    blue.putpixel([i,j],(255,255,255))
                    blueshuju.append(255)
                    haha+=1
                else:
                    blue.putpixel([i,j],(0,0,0))
                    blueshuju.append(0)
                tushuju+=1   
        if haha==0:
            tushuju=0
            for  i in range(r.size[0]):
               for j in range(r.size[1]):
                    if a[tushuju][0]<100 and a[tushuju][1]< 150 and  a[tushuju][2]>150:
                        blue.putpixel([i,j],(255,255,255))
                        haha+=1
                    else:
                        blue.putpixel([i,j],(0,0,0))
                    tushuju+=1  


        #进行滤波处理
        blue=blue.filter(ImageFilter.MinFilter(3))#最小值滤波
        blue=blue.filter(ImageFilter.MaxFilter(9))#最大值滤波

        #接下来要把白色区域识别出来
        tushuju=0
        bai=0
        b=[]
        d=[]
        for  i in range(blue.size[0]):
            for j in range(blue.size[1]):
                b.append(blue.getpixel((i,j)))#得到每一个点的像素值 
        #开始检测
        for  i in range(blue.size[0]):#行扫描
            for j in range(blue.size[1]):
                if b[tushuju][0]==255 and b[tushuju][1]==255 and  b[tushuju][2]==255:
                    bai=bai+1
                tushuju+=1
            if bai>1:
                d.append(i)
                bai=0
                
        tushuju=0

        e=[] 
        bai=0 

        
        for  i in range(blue.size[1]):#列扫描
            for j in range(blue.size[0]):
                if b[tushuju][0]==255 and b[tushuju][1]==255 and  b[tushuju][2]==255:
                    bai=bai+1
                tushuju+=blue.size[1]
            if bai>1:
                e.append(i)
                bai=0
            tushuju=i  
        if len(e)==0 or len(d)==0:
            showinfo(title="错误",message="出了一个错误，请换张图试试！")
            top=0
            down=0
            left=0
            right=0
        else:
            top=e[0]
            down=e[-1]
            left=d[0]
            right=d[-1]
        box=(left,top,right,down)
        imcrox=im.crop(box)
        plt.imshow(imcrox)
        plt.show()

def myyuantu():
    global filename
    myyuantu=Image.open(filename)
    plt.imshow(myyuantu)
    plt.axis('off')
    plt.title=('原图')
    plt.show()

    
#以下是界面部分
def GUI():
    root=Tk()
    root.title('Digtal Image Process')
    root.geometry('500x300') 
    menubar=Menu(root)
    
    #以下为文件菜单内容
    
    #直接在顶级菜单menubar下开始
    filemenu=Menu(menubar)    
    filemenu.add_command(label='打开',command=myopen)
    filemenu.add_command(label='原图',command=myyuantu)
    filemenu.add_command(label='退出',command=myexit)
    
    #以下为车牌定位菜单下面的内容
    chepaimenu=Menu(menubar)
    chepaimenu.add_command(label='定位',command=mychepai)

    #一些为编辑菜单内容
    editmenu=Menu(menubar)
 
   
    editmenu.add_command(label='直方图',command=myzhifangtu)
    editmenu.add_command(label='反转',command=myfanzhuan)
    editmenu.add_command(label='灰度图',command=mygray)
    editmenu.add_command(label='缩络图',command=mysuo)
 

    
    
    #以下为帮助菜单内容
    helpmenu=Menu(menubar)
    helpmenu.add_command(label='关于',command=myguanyu)
    helpmenu.add_command(label='版本',command=mybanben)
    helpmenu.add_command(label='版权',command=mybanquan)
    

    
    #以下为顶级菜单
    menubar.add_cascade(label="文件",menu=filemenu)
    menubar.add_cascade(label="车牌识别",menu=chepaimenu)
    menubar.add_cascade(label="编辑",menu=editmenu)

    menubar.add_cascade(label="帮助",menu=helpmenu)

    root['menu']=menubar
    root.mainloop()
GUI()