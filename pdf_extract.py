# -*- coding: utf-8 -*-

import os
import io
import sys
from PIL import Image

try:
    from PyPDF2 import PdfReader  # 兼容 PyPDF2 新版（>=2.0.0）
except ImportError:
    from PyPDF2 import PdfFileReader as PdfReader  # 兼容 PyPDF2 旧版（<2.0.0）

def extract_images_from_pdf(pdf_path):
    # 获取 PDF 文件所在目录和文件名（不含扩展名）
    pdf_dir = os.path.dirname(pdf_path)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # 创建以 PDF 文件名命名的文件夹
    output_folder = os.path.join(pdf_dir, pdf_name)
    os.makedirs(output_folder, exist_ok=True)

    # 打开 PDF 文件
    pdf_reader = PdfReader(pdf_path)

    # 获取总页数并计算页号的位数
    total_pages = len(pdf_reader.pages)
    page_number_width = len(str(total_pages))

    # 遍历 PDF 每一页
    for page_num in range(total_pages):
        page = pdf_reader.pages[page_num]

        # 检查页面是否包含 XObject（图片对象）
        if "/Resources" in page and "/XObject" in page["/Resources"]:
            xObject = page["/Resources"]["/XObject"]

            # 创建保存当前页图片的子文件夹
            folder_name = os.path.join(output_folder, f"page_{str(page_num + 1).zfill(page_number_width)}_images")
            os.makedirs(folder_name, exist_ok=True)

            # 遍历所有对象
            for obj_name in xObject:
                obj = xObject[obj_name]
                if obj.get("/Subtype") == "/Image":
                    try:
                        # 读取图片数据
                        if hasattr(obj, "get_data"):
                            img_data = obj.get_data()  # 新版 PyPDF2
                        else:
                            img_data = obj._data  # 旧版 PyPDF2
                        
                        img_stream = io.BytesIO(img_data)

                        # 处理图片格式
                        img_format = obj.get("/Filter")
                        ext = "jpg" if img_format == "/DCTDecode" else "png"

                        # 用 PIL 打开图片
                        img = Image.open(img_stream)

                        # 保存图片，文件名加上页号前缀
                        img_filename = os.path.join(
                            folder_name,
                            f"{str(page_num + 1).zfill(page_number_width)}_{obj_name[1:]}.{ext}"
                        )
                        img.save(img_filename)
                        print(f"保存图片: {img_filename}")
                    except Exception as e:
                        print(f"提取图片失败: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        pdf_path = input('请拖入 PDF 文件到终端窗口里,并回车:\n')
        if not pdf_path.strip():
            print("未输入文件路径")
            sys.exit(1)
        else:
            pdf_path = pdf_path.strip('"')
    else:
        pdf_path = sys.argv[1].strip('"')

    if not os.path.isfile(pdf_path):
        print(f"文件不存在: {pdf_path}")
        sys.exit(1)

    extract_images_from_pdf(pdf_path)
    print("图片提取完成！")