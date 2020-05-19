# -*- coding: utf-8 -*-
"""
Created on Wed May  6 11:27:23 2020

@author: kkjb
"""
import fnmatch
import os
import img2pdf
import natsort
import PyPDF2

#pdf批量合并
#当前目录的子目录作为文件民
#子目录自然排序待合并的jpg

# 函数预留 输入 jpg文件目录，输入输出目录
def pdf_converter(full_s_dir,pdf_output_name):
    # get jpg name in s_dir to jpg_list
    jpg_list = fnmatch.filter(os.listdir(full_s_dir), '*.jpg')
    jpg_list = natsort.natsorted(jpg_list)
    for i in range(len(jpg_list)):
        jpg_list[i] = full_s_dir + '\\' + jpg_list[i]
    with open(pdf_output_name,"wb") as f:
    	f.write(img2pdf.convert(jpg_list))
    f.close()
#获取一个目录下的pdf文件名称
#用于合并多个pdf文件    
def pdf_file_name_in_dir(full_s_dir,pdf_output_name):
    pdf_list = fnmatch.filter(os.listdir(full_s_dir), '*.pdf')
    pdf_list = natsort.natsorted(pdf_list)
    for i in range(len(pdf_list)):
        pdf_list[i] = full_s_dir + '\\' + pdf_list[i]
    pdf_output = PyPDF2.PdfFileWriter()
    for file_name in pdf_list:
        pdf_input = PyPDF2.PdfFileReader(open(file_name, 'rb'))
        # 获取 pdf 共用多少页
        page_count = pdf_input.getNumPages()
        #print(page_count)
        for i in range(page_count):
            pdf_output.addPage(pdf_input.getPage(i))
    pdf_output.write(open(pdf_output_name, 'wb'))    


s_root_dir =os.getcwd()
s_dir_list =[f.name for f in os.scandir(s_root_dir) if f.is_dir() ]
full_s_dir_list = []
for i in range(len(s_dir_list)):
    full_s_dir_list.append( s_root_dir + '\\' +s_dir_list[i] )

#jpg到pdf合并
#出错自动跳过
for i in range(len(s_dir_list)):
    pdf_output_name = s_dir_list[i] +".pdf"
    full_s_dir      = full_s_dir_list[i]
    try:
        pdf_converter(full_s_dir,pdf_output_name)
    except Exception as e:
        pass
    continue

#合并多个pdf
#出错自动跳过
for i in range(len(s_dir_list)):
    pdf_output_name = s_dir_list[i] +".pdf"
    full_s_dir      = full_s_dir_list[i]
    try:
        pdf_file_name_in_dir(full_s_dir,pdf_output_name)
    except Exception as e:
        pass
    continue        

