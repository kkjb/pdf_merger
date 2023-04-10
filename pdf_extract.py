# -*- coding: utf-8 -*-
"""
Created on Wed May  6 11:27:23 2020

@author: kkjb
"""
# import fnmatch
# import os
# import img2pdf
# import natsort
# import PyPDF2

# #pdf批量合并
# #当前目录的子目录作为文件民
# #子目录自然排序待合并的jpg

# # 函数预留 输入 jpg文件目录，输入输出目录
# def pdf_converter(full_s_dir,pdf_output_name):
#     # get jpg name in s_dir to jpg_list
#     jpg_list = fnmatch.filter(os.listdir(full_s_dir), '*.png')
#     jpg_list = jpg_list + fnmatch.filter(os.listdir(full_s_dir), '*.jpg')
#     # 自然排序
#     jpg_list = natsort.natsorted(jpg_list)
#     # 补全完整路径
#     for i in range(len(jpg_list)):
#         jpg_list[i] = full_s_dir + '\\' + jpg_list[i]
#     # 打开pdf指针
#     with open(pdf_output_name,"wb") as f:
#     	f.write(img2pdf.convert(jpg_list))
#     f.close()
# # 获取一个目录下的pdf文件名称
# # 用于合并多个pdf文件    
# def pdf_file_name_in_dir(full_s_dir,pdf_output_name):
#     pdf_list = fnmatch.filter(os.listdir(full_s_dir), '*.pdf')
#     pdf_list = natsort.natsorted(pdf_list)
#     for i in range(len(pdf_list)):
#         pdf_list[i] = full_s_dir + '\\' + pdf_list[i]
#     pdf_output = PyPDF2.PdfFileWriter()
#     for file_name in pdf_list:
#         pdf_input = PyPDF2.PdfFileReader(open(file_name, 'rb'))
#         # 获取 pdf 共用多少页
#         page_count = pdf_input.getNumPages()
#         #print(page_count)
#         for i in range(page_count):
#             pdf_output.addPage(pdf_input.getPage(i))
#     pdf_output.write(open(pdf_output_name, 'wb'))    


# s_root_dir =os.getcwd()
# s_dir_list =[f.name for f in os.scandir(s_root_dir) if f.is_dir() ]
# full_s_dir_list = []
# for i in range(len(s_dir_list)):
#     full_s_dir_list.append( s_root_dir + '\\' +s_dir_list[i] )

# #jpg到pdf合并
# #出错自动跳过
# for i in range(len(s_dir_list)):
#     pdf_output_name = s_dir_list[i] +".pdf"
#     full_s_dir      = full_s_dir_list[i]
#     try:
#     # try jpg to pdf at first
#         pdf_converter(full_s_dir,pdf_output_name)
#     except IndexError as e:
#     # if IndexError happens, which means this directory has multi-pdf for mergeing    
#         pdf_file_name_in_dir(full_s_dir,pdf_output_name)
#     continue


# # #合并多个pdf
# # #出错自动跳过

# # for i in range(len(s_dir_list)):
# #     pdf_output_name = s_dir_list[i] +".pdf"
# #     full_s_dir      = full_s_dir_list[i]
# #     try:
# #         pdf_file_name_in_dir(full_s_dir,pdf_output_name)
# #     except Exception as e:
# #         pass
# #     continue        


import PyPDF2
import io
from PIL import Image
import os

# Open the PDF file and create a PDF reader object
pdf_file = open('example.pdf', 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_file)

# Loop through each page in the PDF file
for page_num in range(pdf_reader.numPages):
    # Get the current page and create a PDF page object
    page = pdf_reader.getPage(page_num)
    page_obj = page['/Resources']['/XObject'].getObject()

    # Create a folder for the current page
    folder_name = "page{}_image".format(page_num+1)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Loop through each object in the page object
    for obj_num in page_obj:
        # Check if the object is an image
        if page_obj[obj_num]['/Subtype'] == '/Image':
            try:
                # Extract the image data and create a PIL image object
                img_data = page_obj[obj_num]._data
                img_stream = io.BytesIO(img_data)
                img = Image.open(img_stream)

                # Save the image to a file in the current page's folder
                img.save('page{}_image{}.{}'.format(page_num+1, obj_num, img.format.lower()))
            except Exception as e:
                print(f"Error extracting image from page {page_num+1}, object {obj_num}: {e}")

# Close the PDF file
pdf_file.close()
