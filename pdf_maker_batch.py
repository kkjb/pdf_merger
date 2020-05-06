# -*- coding: utf-8 -*-
"""
Created on Wed May  6 11:27:23 2020

@author: kkjb
"""
import fnmatch
import os
import img2pdf
import natsort

#pdf批量合并
#当前目录的子目录作为文件民
#子目录自然排序待合并的jpg

# 函数预留 输入 jpg文件目录，输入输出目录
def pdf_converter(full_s_dir,pdf_output_name):
    # get jpg name in s_dir to jpg_list
    jpg_list = fnmatch.filter(os.listdir(full_s_dir), '*.jpg')
    jpg_list = natsort.natsorted(jpg_list)
    for i in range(len(jpg_list)):
        jpg_list[i] = full_s_dir + '\\' +jpg_list[i]
    with open(pdf_output_name,"wb") as f:
    	f.write(img2pdf.convert(jpg_list))
    f.close()
    
s_root_dir =os.getcwd()
s_dir_list =[f.name for f in os.scandir(s_root_dir) if f.is_dir() ]
full_s_dir_list = []
for i in range(len(s_dir_list)):
    full_s_dir_list.append( s_root_dir + '\\' +s_dir_list[i] )
    
for i in range(len(s_dir_list)):
    pdf_output_name = s_dir_list[i] +".pdf"
    full_s_dir      = full_s_dir_list[i]
    pdf_converter(full_s_dir,pdf_output_name)
