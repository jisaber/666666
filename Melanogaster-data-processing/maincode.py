#测试各种操作
#!/usr/bin/env python3
#-*- coding:utf-8 -*-

__author__="zhuxiang"

__version__=("0.0.0.0")

__purpose__=r'''Dropsophila-DateProcess'''

__content__=r'''包括了'''

__time__=r'''7天才写出来，我也是醉了，我的cox还没分析好啊'''

__date__=r'''20170714-20170721'''

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
#有一个叫做pyechart的插件，或者echat的库，据说画图很好看，懒得弄了，交给下面的师弟吧
from PIL import Image
import matplotlib.pyplot as plt
from pylab import *
import re



#以下类用于文件操作
import os


#------函数开始-----
global filename
global path
global file
global file1
global ext
global date

global sex
global drug


global sexlist
global xingbie


filename=None
file=None
path=None
file1=None
ext=None

global diris
global fileis

#global filenamelabel


#打开文件对话框并读取一个文件
def myopen():
    global filename
    global path
    global file
    global file1
    global ext
    global date

    global diris#文件的目录
    global fileis#文件的名称
    #global filenamelabel
    
    filename=askopenfilename(defaultextension=".bmp",
        filetypes = [("xls文件",".xls"),("xlsx文件",".xlsx "),("所有文件",".*")])
    #path,file = os.path.split(filename)
    file1,ext = os.path.splitext(filename)
    diris,fileis=os.path.split(filename)
        
def myexit():
    exit()


#以下是帮助模块的内容
    
def myshurumuban():
    #img=Image.open('C:/Users/ZjuTH/Desktop/暑假实验/表格/1.jpg')
    #plt.figure("输入模板")
    #plt.imshow(img)
    #plt.show()
    showinfo(title="模板",message="数据格式必须是.xls不能是.xlsx，数据不能有除数字外的其他任何字符，空格用0代替，最后一列不需要补充0")
    
def myshuchumuban():
    #img=Image.open('C:/Users/ZjuTH/Desktop/暑假实验/表格/2.jpg')
    #plt.figure("输出模板")
    #plt.imshow(img)
    #plt.show()
    showinfo(title="输出",message="计算输出为mean-median-max-min-P值等+画图数据")
def mybanben():
    showinfo(title="版本",message="第一版    version - 0.0.0.1")

def mybanquan():
    showinfo(title="版权",message="版权归制作者所有，未经同意不可以复制！")

def myguanyu():
    showinfo(title="关于",message="朱想制作，品质保证"+'\n'+'其他事宜请查看http://shenjie1858.blog.163.com')
    


#以上的为文件处理模块

#以下的为数据处理模块
sheetname = None

def zhuanhuan():
    global sheetname
    global path
    global file
    global file1
    global ext 
    global date
    global sex
    global drug
    shuju=[]
    tongji=[]
    global filename
    if filename==None:
        showinfo(title="错误提示",message="没有选中文件")
        

    #filename="C://Users//ZjuTH//Desktop//暑假实验//表格//lifespan.xls"
    filedir,filetotalname= os.path.split(filename)
    file1,ext = os.path.splitext(filename)    
    try:
        sample=int(samplex.get())#每组有几管
        sex=int(sexx.get())#有几种性别
        drug=int(drugx.get())#一共有多少浓度
    except Exception as e:
        showinfo(title="状态",message=str(e)+'\n'+'可能没有输入"性别个数"、"每种性别管数"、"药物浓度数"')


    data = xlrd.open_workbook(filename)
    #（2 ，3）才是正式的数据（0 ,0）表示左上角     
    table = data.sheets()[0] # 打开第一张表
    nrows = table.nrows # 获取表的行数
    ncols = table.ncols# 获取表的列数
    sheetname = data.sheet_names()[0]
    #print(data.sheet_names()[0])
    #print(data.nsheets)
    
    #下面两个这个返回的是sheet的指针地址，也就意味着这个返回的是一个表格，
    #可以在这个基础上进行操错，如*.nrows等等
    #print(data.sheet_by_index(1))
    #print(xl.sheet_by_name(u"目录"))
    
    #print(nrows)
    #print(ncols)
    #print(filename)
    #创建workbook和sheet对象
    workbook = xlwt.Workbook() #注意Workbook的开头W要大写
    sheet1 = workbook.add_sheet('统计数据',cell_overwrite_ok=True)
    sheet2 = workbook.add_sheet('画图',cell_overwrite_ok=True)
    #sheet3 = workbook.add_sheet('OASIS',cell_overwrite_ok=True)
    #sheet3= workbook.add_sheet('COX',cell_overwrite_ok=True)

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

    global daylist
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

    global sexlist
    sexlist=[]

    druglist=[]

    global xingbie
    xingbie=[]
    for sexi in range(sex):
        xingbie.append(table.cell(sexi*sample+2,2).value)

    global nongdu
    nongdu = []
   
    for drugi in range(drug):
        nongdu.append(table.cell(drugi*sex*sample+2,1).value)
        #print(nongdu)l老铁没毛病

    try:
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
            
    except Exception as e:
        showinfo(title="状态",message=str(e)+'\n'+'"性别个数"、"每种性别管数"、"药物浓度数"可能输入错误、或者原始数据中有空白')


    




    global survivallist2
    #global xingbie
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
    #这个数据可以用来做COX
    for sexi in range(sex):
        for drugi in range(drug):
                #以下部分完成一种浓度的一种性别的处理
            for dayi in range(ncols-3):
                #print(sexlist[sexi][drugi][dayi])
                for i in range(int(sexlist[sexi][drugi][dayi])):
                    templist.append(daylist[dayi])
                    templist2.append(1)

            #一个浓度转换完成
            datalist.append(nongdu[drugi])
            #这个时候就把原先的0，1，2.。。换成对照，最低之类的单词

            datalist.append(re.sub('[^a-zA-Z]','',xingbie[sexi]))
            
            datalist.append(len(templist))
            datalist.append(np.mean(templist))
            datalist.append(np.median(templist))
            datalist.append(np.min(templist).tolist())
            datalist.append(np.max(templist).tolist())
            #print("\n")

            #这两个是用来画图用和计算P-value的
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
    #下面是P值的数据
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


    #以下为画图模块的数据
    #需要几张图
    sexlisttu=[]

    tempsexlisttu=[]

    global tempsexlisttu1
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

   
   


    
    #以下用于写画图用的数据
    sheet2.write(0,0,'DAY')#写DAY

    for sexi in range(sex):
        #写第一行的标题
        #2018.03.01修改为动态显示不是固定的F11之类的，改成F对照组
        #这里使用了一次正则表达式去掉F1里面的1
        for drugi in range(drug):
            sheet2.write(0,sexi*drug+drugi+1,
                         re.sub('[^a-zA-Z]','',str(xingbie[sexi]))+str(nongdu[drugi]))        

    for i in range(len(daylist)):
        sheet2.write(i+1,0,daylist[i])

    for sexi in range(sex): #按行处理
        for drugi in range(drug):
            for i in range(len(daylist)):
                sheet2.write(i+1,sexi*drug+drugi+1,
                             tempsexlisttu1[sexi][drugi][i])


                
    #再输出图片
    #画图之前需要转换成存活率
    

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
    #20180301修改，添加了一个全局变量button控制计算次数，每次计算都会重新生成新的文件
    try:
        workbook.save(file1+str(sheetname)+'Data'+ext)
        showinfo(title="状态",message="处理成功！文件目录:"+'\n'+file1)
    except Exception as e:
        showinfo(title="状态",message=str(e)+'\n'+'可能相同文件名的文件已经在Excel中打开，请关闭之后再试试')

def myOASIS():
    global daylist
    global xingbie
    global sex
    global drug
    global sexlist
    #以下用于OASIS，因为OASIS和性别有关，所以需要重新建一个文档
    workbookOASIS = xlwt.Workbook() #注意Workbook的开头W要大写
    sheet=[]
    try:
        lendaylist=len(daylist)
    except Exception as e:
        showinfo(title="状态",message=str(e)+'\n'+'先计算之后再产生OASIS')
    
    for sexi in range(sex):
        sheet.append(workbookOASIS.add_sheet(str(xingbie[sexi]),
                                         cell_overwrite_ok=True))
    for sexi in range(sex):
        for drugi in range(drug):
            sheet[sexi].write(drugi*(lendaylist+2),0,
                              '%'+str(xingbie[sexi])+str(drugi))
            sheet[sexi].write(drugi*(lendaylist+2)+1,0,
                              '#Day')
            sheet[sexi].write(drugi*(lendaylist+2)+1,1,
                              'dead')
            sheet[sexi].write(drugi*(lendaylist+2)+1,2,
                              'censored')
            for i in range(lendaylist):
                sheet[sexi].write(drugi*(lendaylist+2)+2+i,0,
                                  daylist[i])
                sheet[sexi].write(drugi*(lendaylist+2)+2+i,1,
                                  sexlist[sexi][drugi][i])  

    try:
        workbookOASIS.save(file1+str(sheetname)+'OASIS'+ext)
        showinfo(title="状态",message='保存OASIS成功,文件目录为：'+'\n'+file1)
    except Exception as e:
        showinfo(title="状态",message=str(e)+'\n'+'保存OASIS失败'+'\n'+'可能相同文件名的文件已经在Excel中打开，请关闭之后再试试')

global survivallist2
global xingbie


def myCOX():
    global sex
    global drug

    global survivallist2
    global xingbie
    #以下用于OASIS，因为OASIS和性别有关，所以需要重新建一个文档
    workbookCOX = xlwt.Workbook() #注意Workbook的开头W要大写
    sheet1 = workbookCOX.add_sheet('COX',cell_overwrite_ok=True)

    sheet1.write(0,0,'#Day')
    sheet1.write(0,1,'dead')
    sheet1.write(0,2,'Sex')
    sheet1.write(0,3,'Drug')
    tempsum=1
    try:
        for i in range(sex):
            pass
    except Exception as e:
        showinfo(title="状态",message=str(e)+'\n'+'先计算之后再产生COX')
    for sexi in range(sex):
        for drugi in range(drug):   
            for i in range(len(survivallist2[sexi][drugi])):
                sheet1.write(tempsum+i,0,survivallist2[sexi][drugi][i])#day的数据
                sheet1.write(tempsum+i,1,1)#这个就是1
                sheet1.write(tempsum+i,2,str(xingbie[sexi]))#这个是SEX
                sheet1.write(tempsum+i,3,drugi)#这个是Drug
            tempsum=tempsum+len(survivallist2[sexi][drugi])
    
    
    try:
        workbookCOX.save(file1+str(sheetname)+'COX'+ext)
        showinfo(title="状态",message='保存COX成功,文件目录为：'+'\n'+file1)
    except Exception as e:
        showinfo(title="状态",message=str(e)+'\n'+'保存COX失败'+'\n'+'可能相同文件名的文件已经在Excel中打开，请关闭之后再试试')



def myhuatu():
    #下面是作图的代码
    global sex
    global drug
    global tempsexlisttu1
    global daylist
    global xingbie

    marklist=['o','s','*','d','_','+','D','x','<','>','v','^']#最多画12条线
    colorlist=['b','black','orange','r','c','k','m','w','y','pink','darkseagreen','seagreen']#最多12种颜色
    try:
        for sexi in range(sex):
            figure(xingbie[sexi])
            
            for drugi in range(drug):

                plt.plot(daylist,tempsexlisttu1[sexi][drugi],marklist[drugi],linestyle='-',color=colorlist[drugi],linewidth=2,label=drugi)
                #plt.plot(daylist,tempsexlisttu1[sexi][drugi],linewidth=2.5,label=drugi)
                
            plt.xlabel('Age(Day)')
            plt.ylabel('Percent Survival')
            plt.title(xingbie[sexi])

            legend(loc='upper right')

            figure(xingbie[sexi]).show()
    except Exception as e:
        showinfo(title="状态",message=str(e)+'\n'+'需要先计算之后才能画图')
        
from tkinter import *
global fileis
def myzidongtianru():
    sexx.set(3)
    samplex.set(3)
    drugx.set(4)
def myqingchu():
    sexx.set(0)
    samplex.set(0)
    drugx.set(0)
def submit():
    print(u.get())
    p.set(u.get())

def mywenjianming():
    showinfo(title="状态",message=fileis)
#def GUI():
root=Tk()
root.title('统计数据计算')
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




frame = Frame(root)
frame.pack(padx=8, pady=8, ipadx=4)

lab1 = Label(frame, text="性别个数")
lab1.grid(row=0, column=0,sticky='w')

sexx = StringVar()
ent1 = Entry(frame, textvariable=sexx,width = 10)
ent1.grid(row=0, column=1, sticky='w')

buttonopen = Button(frame, text="打开文件", command=myopen)
buttonopen.grid(row=0, column=2,sticky='w')

lab2 = Label(frame, text="每种性别管数")
lab2.grid(row=1, column=0,  sticky='w')

samplex = StringVar()
ent2 = Entry(frame, textvariable=samplex,width = 10)
ent2.grid(row=1, column=1, sticky='w')

lab3 = Label(frame, text="药物浓度数")
lab3.grid(row=2, column=0,  sticky=W)

drugx = StringVar()
ent3 = Entry(frame, textvariable=drugx,width = 10)
ent3.grid(row=2, column=1, sticky='w')

button1 = Button(frame, text="自动填入", command=myzidongtianru)
button1.grid(row=3, column=0,sticky='w')

button11 = Button(frame, text="自动清除", command=myqingchu)
button11.grid(row=4, column=0,sticky='w')

button2 = Button(frame, text="计算",command=zhuanhuan, default='active')
button2.grid(row=3, column=1,sticky='w')

button5 = Button(frame, text="OASIS",command=myOASIS)
button5.grid(row=4, column=1,sticky='w')

button7 = Button(frame, text="COX",command=myCOX)
button7.grid(row=4, column=2,sticky='w')

button6 = Button(frame, text="画图",command=myhuatu)
button6.grid(row=4, column=3,sticky='w')

button4 = Button(frame, text="退出", command=quit)
button4.grid(row=0, column=3,sticky='w')

buttonfile = Button(frame, text="当前文件", command=mywenjianming)
buttonfile.grid(row=1, column=2,sticky='w')



root.iconbitmap('D:\\100.ico')
root.mainloop()
