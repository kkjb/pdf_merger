# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import natsort
import fnmatch
import string
import shutil

full_s_dir = os.getcwd()

os.chdir(full_s_dir)

pdf_list = fnmatch.filter(os.listdir(full_s_dir), '*.pdf')
pdf_list = natsort.natsorted(pdf_list)

for i in range(len(pdf_list)):
    # rm .pdf 后缀
    dirname = pdf_list[i][0:-4]
    # rm 行尾数字
    dirname = dirname.rstrip(string.digits)
    
    
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
        
    old_path = full_s_dir + "\\" + pdf_list[i]
    new_path = full_s_dir + "\\" + dirname + "\\" + pdf_list[i]
    shutil.move(old_path,new_path)


'''
pdf_no_suffix_list =[]
for i in range(len(pdf_list)):
    # rm .pdf 后缀
    pdf_no_suffix_list.append( pdf_list[i][0:-4])
    #print(pdf_no_suffix_list[i])
    # rm 行尾数字
    
    pdf_no_suffix_list[i] = pdf_no_suffix_list[i].rstrip(string.digits)
    #print(pdf_no_suffix_list[i])
    
#去重复    
directory_name = list(set(pdf_no_suffix_list))

#切换目录

os.chdir(full_s_dir)
for i in range(len(directory_name)):
    os.mkdir(directory_name[i])

for i in range(len(pdf_list)):
    pdf_name = pdf_list[i][0:-4]
    for 

'''