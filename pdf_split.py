# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import PyPDF2
import re
import os
import sys
import time
import natsort
import pikepdf  # 用于压缩PDF

# 自然排序

# PDF分割函数
def split_pdf(input_pdf, end_pages, compress=False):
    # 获取输入PDF的路径和文件名
    input_dir = os.path.dirname(input_pdf)
    input_filename = os.path.basename(input_pdf)

    print(f"输入文件路径: {input_pdf}")
    print(f"文件所在目录: {input_dir}")

    # 创建一个新的文件夹 'split' 来存储分割后的文件
    split_dir = os.path.join(input_dir, "split")
    if not os.path.exists(split_dir):
        try:
            os.makedirs(split_dir)
            print(f"创建文件夹成功: {split_dir}")
        except Exception as e:
            print(f"创建文件夹失败: {e}")
            return

    # 使用 PdfFileReader 而非 PdfReader
    with open(input_pdf, "rb") as f:
        reader = PyPDF2.PdfFileReader(f)
        total_pages = reader.getNumPages()

        print(f"总页数: {total_pages}")

        # 确保输入的分割页数从小到大排序
        end_pages = natsort.natsorted(end_pages)

        # 计算每个分割段的起始页和结束页
        start_page = 0  # PyPDF2的页码从0开始
        for end in end_pages:
            if end > total_pages:
                print(f"错误：页码 {end} 超出总页数 {total_pages}.")
                continue

            writer = PyPDF2.PdfFileWriter()
            # 添加每个分割段的页面
            for i in range(start_page, end):
                writer.addPage(reader.getPage(i))

            # 输出文件路径
            output_filename = f"output_{start_page + 1}-{end}.pdf"
            output_filepath = os.path.join(split_dir, output_filename)

            try:
                # 写入分割后的PDF文件
                with open(output_filepath, "wb") as output_pdf:
                    writer.write(output_pdf)
                print(f"文件 {output_filename} 创建成功! 保存路径：{output_filepath}")

                # 如果选择了压缩选项，则进行压缩
                if compress:
                    compress_pdf(output_filepath)

            except Exception as e:
                print(f"保存文件失败: {e}")
                continue

            # 更新下一段的起始页为当前分割段的结束页
            start_page = end  # 下一段的起始页为当前分割段的结束页

        # 如果有剩余的页面（未包含在分割点内），保存最后一段
        if start_page < total_pages:
            writer = PyPDF2.PdfFileWriter()
            for i in range(start_page, total_pages):
                writer.addPage(reader.getPage(i))

            output_filename = f"output_{start_page + 1}-{total_pages}.pdf"
            output_filepath = os.path.join(split_dir, output_filename)

            try:
                with open(output_filepath, "wb") as output_pdf:
                    writer.write(output_pdf)
                print(f"文件 {output_filename} 创建成功! 保存路径：{output_filepath}")

                # 如果选择了压缩选项，则进行压缩
                if compress:
                    compress_pdf(output_filepath)

            except Exception as e:
                print(f"保存文件失败: {e}")
                return

# 压缩PDF文件
def compress_pdf(input_pdf):
    try:
        with pikepdf.open(input_pdf, allow_overwriting_input=True) as pdf:
            pdf.save(input_pdf, compress_streams=True)  # 开启压缩选项
        print(f"文件已压缩: {input_pdf}")
    except Exception as e:
        print(f"压缩文件失败: {e}")

# 主函数
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("请拖拽PDF文件到命令行窗口，或手动输入文件路径。")
        path_name = input('请输入PDF文件路径:\n')
        
        if path_name == '':
            print("没有输入路径，程序退出。")
            time.sleep(5)
            exit()
        else:
            pdf_file = path_name.strip('"')
            input_ranges = input(f"请输入分割点位置（最后一页，空格分隔） for {pdf_file}: ")
            compress_option = input("是否压缩分割后的PDF文件? (yes/no): ").strip().lower()
            compress = compress_option == 'yes'

            if input_ranges:
                end_pages = list(map(int, input_ranges.split()))
                split_pdf(pdf_file, end_pages, compress)
            else:
                print("没有输入分割点，程序退出。")
                time.sleep(5)
                exit()

    else:
        pdf_file = sys.argv[1].strip('"')
        input_ranges = input(f"请输入分割点位置（最后一页，空格分隔） for {pdf_file}: ")
        compress_option = input("是否压缩分割后的PDF文件? (yes/no): ").strip().lower()
        compress = compress_option == 'yes'

        if input_ranges:
            end_pages = list(map(int, input_ranges.split()))
            split_pdf(pdf_file, end_pages, compress)
        else:
            print("没有输入分割点，程序退出。")
            time.sleep(5)
            exit()
