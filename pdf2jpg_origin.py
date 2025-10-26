import fitz  # PyMuPDF
import os
import sys

def extract_images_from_pdf(pdf_path):
    """从 PDF 中提取所有嵌入的图片"""
    output_dir = os.path.splitext(pdf_path)[0] + "_images"
    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(pdf_path)
    img_count = 0

    for page_index, page in enumerate(doc):
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_name = f"p{page_index + 1}_img{img_index + 1}.{image_ext}"

            with open(os.path.join(output_dir, image_name), "wb") as f:
                f.write(image_bytes)

            img_count += 1

    print(f"共提取 {img_count} 张图片，保存在目录: {output_dir}")
    doc.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        pdf_path = input('请拖入 PDF 文件到终端窗口里, 并回车:\n').strip()
    else:
        pdf_path = sys.argv[1]

    # ---- 修复重点部分 ----
    # 1. 去掉路径首尾的引号
    pdf_path = pdf_path.strip('"').strip("'")

    # 2. 去掉 Windows 的转义字符
    pdf_path = os.path.normpath(pdf_path)

    # 3. 确认文件是否存在
    if not os.path.isfile(pdf_path):
        print(f"文件不存在或路径无效:\n{pdf_path}")
        input("按回车退出...")
        sys.exit(1)

    extract_images_from_pdf(pdf_path)
    print("图片提取完成！")
    input("按回车退出...")
