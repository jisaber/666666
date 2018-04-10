#测试各种操作
#!/usr/bin/env python3
#-*- coding:utf-8 -*-

__author__="zhuxiang"

__version__=("0.0.0.0")

__purpose__=r'''Dropsophila-DateProcess'''

__content__=r'''包括了'''

__time__=r'''4天才写出来，我也是醉了，我的cox还没分析好啊'''

__date__=r'''20170714-20170718'''

#以下类用于界面
from tkinter import*
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import *






#以下用于数据处理
import xlrd#用于数据的读
import xlwt#用于数据的写

import numpy as np
import pandas as pd

#from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test




#以下类用于画图
from PIL import Image
import matplotlib.pyplot as plt
from pylab import *



#以下类用于文件操作
import os
#------函数开始-----
global filename
global path
global file
global file1
global ext
global date

filename=None
file=None
path=None
file1=None
ext=None


#打开文件对话框并读取一个文件
def myopen():
    global filename
    global path
    global file
    global file1
    global ext
    global date
    filename=askopenfilename(defaultextension=".bmp",
        filetypes = [("xls文件",".xls"),("xlsx文件",".xlsx "),("所有文件",".*")])
    #path,file = os.path.split(filename)
    file1,ext = os.path.splitext(filename)    
        
def myexit():
    exit()


#以下是帮助模块的内容
    
def myshurumuban():
    #img=Image.open('C:/Users/ZjuTH/Desktop/暑假实验/表格/1.jpg')
    plt.figure("输入模板")
    plt.imshow(img)
    plt.show()
def myshuchumuban():
    #img=Image.open('C:/Users/ZjuTH/Desktop/暑假实验/表格/2.jpg')
    plt.figure("输出模板")
    plt.imshow(img)
    plt.show()
def mybanben():
    showinfo(title="版本",message="第一版    version - 0.0.0.1")

def mybanquan():
    showinfo(title="版权",message="版权归制作者所有，未经同意不可以复制！")

def myguanyu():
    showinfo(title="关于",message="朱想制作，品质保证")
    


#以上的为文件处理模块

#以下的为数据处理模块 

def zhuanhuan():
    shuju=[]
    tongji=[]
    global filename

    #filename="C://Users//ZjuTH//Desktop//暑假实验//表格//lifespan.xls"
    file1,ext = os.path.splitext(filename)
    global path
    global file
    global file1
    global ext
    global date
    sample=2#每组有几管
    sex=3#有几种性别
    drug=4#一共有多少浓度


    data = xlrd.open_workbook(filename)
    #（2 ，3）才是正式的数据（0 ,0）表示左上角     
    table = data.sheets()[0] # 打开第一张表
    nrows = table.nrows # 获取表的行数
    ncols = table.ncols# 获取表的列数
    print(nrows)
    print(ncols)
    print(filename)
    #创建workbook和sheet对象
    workbook = xlwt.Workbook() #注意Workbook的开头W要大写
    sheet1 = workbook.add_sheet('统计数据',cell_overwrite_ok=True)
    sheet2 = workbook.add_sheet('OASIS',cell_overwrite_ok=True)

    #以下是处理的核心部分

    #先进行各项统计数据的处理
    temp=[]

    for i in range(nrows-1):
        for j in range(ncols-3):
            temp.append(table.cell(i+1,j+3).value)
            #包含了DAY的信息shuju[0]就是DAY的信息    
        shuju.append(temp)
        temp=[]
    #print(shuju[26][16])
    df = pd.DataFrame(shuju)
    dftemp=df.ix[1:sex*sample*drug,:]#得到除DAY信息之外的数据
    #print(df.ix[24,16])
    #print(dftemp.ix[0,:])
    #r'''


    daylist=[]
    for dayi in range(ncols-3):
        daylist.append(dayi*2)

        
    #print(daylist)

    #print(dftemp.head())
    #shuju这个list是一个二维数组
    sexshuju=[]
    sampleshuju=[]
    durgshuju=[]

    tempsum=0

    templist=[]

    tempzonghelist=[]

    samplelist=[]

    sexlist=[]

    druglist=[]

    xingbie=[]
    for sexi in range(sex):
        xingbie.append(table.cell(sexi*sample+2,2).value)

    for sexi in range(sex):
        for drugi in range(drug):
            #以下部分完成一种浓度的一种性别的相加
            for j in range(ncols-3):
                for samplei in range(sample):
                    tempx=1+int(samplei+sexi*sample+sample*sex*drugi)
                    #print(j)
                    #print(tempx)
                    #break
                    tempsum=tempsum+int(shuju[tempx][j])
                    #sexi*3决定开始的时候从第几个开始
                    #Sample*sex*drugi决定了每次跳过多少个进行下一组药的计算
                    
                templist.append(tempsum)#遍历完成第一行矩阵已经完成
                tempsum=0

            druglist.append(templist)
            templist=[]
        sexlist.append(druglist)#这个时候得到最顶端的那个list
        druglist=[]

    #开始得到数据
    #df1 = pd.DataFrame(sexlist)
    templist=[]
    templist2=[]
    eventlist=[]
    eventlist2=[]
    survivallist=[]
    survivallist2=[]

    datalist=[]
    drugdatalist=[]
    sexdatalist=[]

    #以下部分是各种统计数据的地方
    for sexi in range(sex):
        for drugi in range(drug):
                #以下部分完成一种浓度的一种性别的处理
            for dayi in range(ncols-3):
                #print(sexlist[sexi][drugi][dayi])
                for i in range(int(sexlist[sexi][drugi][dayi])):
                    templist.append(daylist[dayi])
                    templist2.append(1)
            #一个浓度转换完成
            datalist.append(drugi)
                    
            datalist.append(xingbie[sexi])
            
            datalist.append(len(templist))
            datalist.append(np.mean(templist))
            datalist.append(np.median(templist))
            datalist.append(np.min(templist).tolist())
            datalist.append(np.max(templist).tolist())
            #print("\n")
            eventlist.append(templist2)
            survivallist.append(templist)


            drugdatalist.append(datalist)
            datalist=[]
            
            templist=[]
            templist2=[]
           
        eventlist2.append(eventlist)
        survivallist2.append(survivallist)
                            
        sexdatalist.append(drugdatalist)
        drugdatalist=[]
        

        
        eventlist=[]
        survivallist=[]
    #print(sexdatalist)

    pvalue=[]
    pvalue1=[]

    for sexi in range(sex):
        pvalue.append('-')
        for drugi in range(drug-1):    
            results = logrank_test(
                                    np.transpose(survivallist2[sexi][0]),
                                    np.transpose(survivallist2[sexi][drugi+1]),
                                    event_observed_A=np.transpose(eventlist2[sexi][0]),
                                    event_observed_B=np.transpose(eventlist2[sexi][drugi+1])

                                   )
            pvalue.append(results.p_value)
            
        pvalue1.append(pvalue)
        pvalue=[]
    #print(pvalue1)
            



            
        

    #把所有的数据区域存到一个list里面便于操作，不然每次都要cell操作很麻烦


    #以下为画图模块吧
    #需要几张图

    #画图之前需要转换成存活率
    sexlisttu=[]

    tempsexlisttu=[]

    tempsexlisttu1=[]

    tempdruglisttu=[]

    temp=0
    temp1=0
    for sexi in range(sex):
        
        for drugi in range(drug):
            temp=sum(sexlist[sexi][drugi])
            temp1=temp
            
            tempdruglisttu.append(100)#第0天的存活率肯定是1
            
            for i in range(1,len(sexlist[sexi][drugi])):
                #下面是第i天的存活率
                temp=temp-sexlist[sexi][drugi][i]
                tempdruglisttu.append(temp/temp1*100)
            #print(len(tempdruglisttu))
            #print(len(daylist))
                
            tempsexlisttu.append(tempdruglisttu)
            tempdruglisttu=[]
        
        #figure(sexi).show()    
        tempsexlisttu1.append(tempsexlisttu)
        tempsexlisttu=[]

    marklist=['o','s','*','d','_','+','D','x','<','>','v','^']#最多画12条线
    colorlist=['b','g','r','y','c','k','m','w']#最多8种颜色

    '''    
    for sexi in range(sex):
        figure(sexi)
        
        for drugi in range(drug):

            plt.plot(daylist,tempsexlisttu1[sexi][drugi],marklist[drugi],linestyle='-',linewidth=2.5,label=drugi)
            #plt.plot(daylist,tempsexlisttu1[sexi][drugi],linewidth=2.5,label=drugi)
            
        plt.xlabel('Age(Day)')
        plt.ylabel('Percent Survival')
        plt.title(xingbie[sexi])

        legend(loc='upper right')

        figure(sexi).show()
    #再输出图片
    '''

    biaoti=['Diet','Drug(Mol/L)','sex','N','Mean','Median','Min','Max','△Mean','△Median','p value']
    for i in range(11):
        #第一行是标题栏
        sheet1.write(0,i,biaoti[i])
    #以下用于写各种数据    
    for sexi in range(sex): #按行处理
        for drugi in range(drug):
            for j in range(7):
                sheet1.write(sexi*drug+drugi+1,j+1,
                             sexdatalist[sexi][drugi][j])
            if drugi==0:
                sheet1.write(sexi*drug+drugi+1,8,'-')
                sheet1.write(sexi*drug+drugi+1,9,'-')
            else:
                sheet1.write(sexi*drug+drugi+1,8,
                             (sexdatalist[sexi][drugi][3]-sexdatalist[sexi][0][3])/sexdatalist[sexi][0][3]*100)

                sheet1.write(sexi*drug+drugi+1,9,
                             (sexdatalist[sexi][drugi][4]-sexdatalist[sexi][0][4])/sexdatalist[sexi][0][4]*100)
                


    #以下用于写P值
    for sexi in range(sex):
        for drugi in range(drug):
                sheet1.write(sexi*drug+drugi+1,10,pvalue1[sexi][drugi])
                

            
            



            

    #保存该excel文件,有同名文件时直接覆盖
    try:
        workbook.save(file1+'Data'+ext)
        showinfo(title="状态",message="处理成功！文件目录:"+'\n'+file1)
    except Exception as e:
        showinfo(title="状态",message=str(e)+'\n'+'可能相同文件名的文件已经打开，请关闭之后再试试')

 
def GUI():
    root=Tk()
    root.title('Scource to Survcur')
    root.geometry('500x300')
    menubar=Menu(root)
    
    
    #以下为文件菜单内容
    
    #直接在顶级菜单menubar下开始
    filemenu=Menu(menubar)

    #以下为文件菜单下面的内容
    filemenu.add_command(label='打开',command=myopen)
    filemenu.add_command(label='退出',command=myexit)
    
    #以下为转换菜单下面的内容
    chepaimenu=Menu(menubar)
    chepaimenu.add_command(label='数据处理',command=zhuanhuan)

    
    #以下为帮助菜单内容
    helpmenu=Menu(menubar)

    helpmenu.add_command(label='输入模板',command=myshurumuban)
    helpmenu.add_command(label='输出模板',command=myshuchumuban)
    helpmenu.add_command(label='关于',command=myguanyu)
    helpmenu.add_command(label='版本',command=mybanben)
    helpmenu.add_command(label='版权',command=mybanquan)
    
 
    
    #以下为顶级菜单
    menubar.add_cascade(label="文件",menu=filemenu)
    menubar.add_cascade(label="数据处理",menu=chepaimenu)
    menubar.add_cascade(label="帮助",menu=helpmenu)   

    root['menu']=menubar
    root.iconbitmap('D:\\100.ico')
    root.mainloop()
GUI()

