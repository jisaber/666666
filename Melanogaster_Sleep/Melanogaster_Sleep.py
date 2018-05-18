#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#测试各种操作

__author__="zhuxiang"

__version__=("0.0.0.0")

__purpose__=r'''Dropsophila-SleepDateProcess'''

__content__=r'''包括了30分钟内睡眠时间，每个睡眠时间段内的平均睡眠时间，总的睡眠时间，睡眠次数，醒来的时候的每分钟活动性'''

__time__=r'''半天完成'''

__date__=r'''20180518 13:00:00 - 17:30:00'''

__declaration__ = r'''输入格式貌似不需要特殊的定义，基本能满足所有的需求'''

from tkinter import*
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import *

import os
import xlwt,xlrd
filename = None
file=None
path=None
file1=None
ext=None
def myopen():
    global filename
    global path
    global file
    global file1
    global ext
    global date

    global diris#文件的目录
    global fileis#文件的名称
    
    filename=askopenfilename(defaultextension=".xls",
        filetypes = [("xls文件",".xls"),("xlsx文件",".xlsx "),("所有文件",".*")])
    file1,ext = os.path.splitext(filename)
    diris,fileis=os.path.split(filename)


SLEEP_TIME_DEFINE = 1#5分钟及以上为0才算作睡眠

start = 0
end = 0

sheetname = None
def process_main():
    print('-------------------- go --------------------')
    # file1,ext = os.path.splitext(filename)
    # diris,fileis=os.path.split(filename)
    try:
        data = xlrd.open_workbook(filename)
        table = data.sheets()[0]
        sheetname = data.sheet_names()[0]
    except:
        showinfo(title="error",message="erro------r")


    #创建workbook和sheet对象
    try:
        workbook = xlwt.Workbook() #注意Workbook的开头W要大写
        sheet1_sleep_for_30min = workbook.add_sheet('30分睡眠数据',cell_overwrite_ok=True)
        sheet1_total_sleep = workbook.add_sheet('总睡眠时间',cell_overwrite_ok=True)
        sheet1_sleep_bout_duration = workbook.add_sheet('睡眠间隔时间',cell_overwrite_ok=True)
        sheet1_number_of_sleep_bouts = workbook.add_sheet('睡眠次数',cell_overwrite_ok=True)
        sheet1_waking_activity = workbook.add_sheet('醒的时候每分钟活动次数',cell_overwrite_ok=True)
    except:
        showinfo(title="error",message="erro------r")

    sleep_30min_results = []
    total_30min_sleep = [0 for i in range(32)]
    tempdiff = [0 for i in range(32)]
    for i in range(table.nrows):
        for j in range(10,42):
            if table.cell(i,j).value == 0:
                tempdiff[j-10] += 1 
            else:
                if tempdiff[j-10] > SLEEP_TIME_DEFINE - 1:
                    total_30min_sleep[j-10] += tempdiff[j-10]
                tempdiff[j-10] = 0
        if i % 30 == 0 and i > 0 or i == table.nrows-1:
            sleep_30min_results.append(total_30min_sleep)
            total_30min_sleep = [0 for i in range(32)]
            tempdiff = [0 for i in range(32)]

    for i in range(int(table.nrows/30)):
        for j in range(32):
            sheet1_sleep_for_30min.write(i+1,j+1,sleep_30min_results[i][j])
    



    #------------------------------------------------------------------#
    total_sleep = [0 for i in range(32)]
    tempdiff = [0 for i in range(32)]
    for i in range(table.nrows):
        for j in range(10,42):
            if table.cell(i,j).value == 0:
                tempdiff[j-10] += 1 
            else:
                if tempdiff[j-10] > SLEEP_TIME_DEFINE - 1:
                    total_sleep[j-10] += tempdiff[j-10]
                tempdiff[j-10] = 0
    for j in range(32):
        sheet1_total_sleep.write(1,j+1,total_sleep[j])
    


    #------------------------------------------------------------------#
    total_sleep_bout_duration = [[] for i in range(32)]
    total_sleep_bout_duration_use = [0 for i in range(32)]
    total_sleep = [0 for i in range(32)]
    tempdiff = [0 for i in range(32)]
    number_of_sleep_bouts = [0 for i in range(32)]
    for i in range(table.nrows):
        for j in range(10,42):
            if table.cell(i,j).value == 0:
                tempdiff[j-10] += 1 
            else:
                if tempdiff[j-10] > SLEEP_TIME_DEFINE - 1:
                    total_sleep[j-10] += tempdiff[j-10]
                    total_sleep_bout_duration[j-10].append(total_sleep[j-10])
                    total_sleep[j-10] = 0
                tempdiff[j-10] = 0

    for i in range(32):
        number_of_sleep_bouts1 = len(total_sleep_bout_duration[i])
        if number_of_sleep_bouts1 == 0:
            number_of_sleep_bouts[i] = 0
        else:
            number_of_sleep_bouts[i] = number_of_sleep_bouts1
            total_sleep_bout_duration_use[i] = sum(total_sleep_bout_duration[i])/number_of_sleep_bouts1
    for j in range(32):
        sheet1_sleep_bout_duration
        sheet1_number_of_sleep_bouts.write(1,j+1,number_of_sleep_bouts[j])
        sheet1_sleep_bout_duration.write(1,j+1,total_sleep_bout_duration_use[j])

    #------------------------------------------------------------------#
    waking_activity = [0 for i in range(32)]
    active = [[0 for j in range(32)] for i in range(table.nrows)]
    for i in range(table.nrows):
        for j in range(10,42):
            active [i][j-10] += table.cell(i,j).value
    
    total_time = table.nrows
    for j in range(32):
        waking_activity[j] = sum([i[j] for i in active])/(total_time - total_sleep[j])
        sheet1_waking_activity.write(1,j+1,waking_activity[j])
           

    try:
        workbook.save(file1+str(sheetname)+'-'+'sleep'+ext)
        showinfo(title="状态",message="处理成功！文件目录:"+'\n'+file1)
    except Exception as e:
        showinfo(title="状态",message=str(e)+'\n'+'可能相同文件名的文件已经在Excel中打开，请关闭之后再试试')

def mywenjianming():
    showinfo(title="状态",message=fileis)

def GUI():
    
    root=Tk()
    root.title('Drosophlia-Melanogaster-Sleep-Analyze')
    root.geometry('500x300')
    frame = Frame(root)
    frame.pack(padx=8, pady=8, ipadx=4)


    buttonopen = Button(frame, text="打开文件", command=myopen)
    buttonopen.grid(row=3, column=1,sticky='w')

    buttonopen = Button(frame, text="计算", command=process_main)
    buttonopen.grid(row=3, column=2,sticky='w')


    buttonfile = Button(frame, text="当前文件", command=mywenjianming)
    buttonfile.grid(row=3, column=3,sticky='w')

    button4 = Button(frame, text="退出", command=quit)
    button4.grid(row=3, column=4,sticky='w')

    root.mainloop()
if __name__ == '__main__':
    GUI()
