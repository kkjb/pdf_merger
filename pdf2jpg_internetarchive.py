import fitz  # PyMuPDF
from PIL import Image
import io
import os

def export_pdf_to_jpg(pdf_path, target_dpi=300, quality=95):
    """
    将 PDF 每一页导出为 300 DPI JPG 图片，尺寸精确匹配页面物理大小
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"文件不存在: {pdf_path}")

    # 输出目录
    output_dir = os.path.splitext(pdf_path)[0] + "_jpg"
    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(pdf_path)
    num_pages = len(doc)
    try:
        for page_index in range(len(doc)):
            page = doc[page_index]

            # PDF 页面尺寸（points）
            rect = page.rect
            page_width_pt = rect.width
            page_height_pt = rect.height

            # 转 inch
            width_inch = page_width_pt / 72
            height_inch = page_height_pt / 72

            # 计算像素尺寸
            pix_width = int(width_inch * target_dpi)
            pix_height = int(height_inch * target_dpi)

            # 计算缩放系数
            zoom_x = pix_width / page_width_pt
            zoom_y = pix_height / page_height_pt
            mat = fitz.Matrix(zoom_x, zoom_y)

            # 渲染 Pixmap
            pix = page.get_pixmap(matrix=mat, alpha=False)

            # 转成 PIL Image
            img = Image.open(io.BytesIO(pix.tobytes("ppm")))

            # 保存 JPG，设置 DPI metadata
            out_file = os.path.join(output_dir, f"page_{page_index + 1}.jpg")
            img.save(out_file, "JPEG", quality=quality, dpi=(target_dpi, target_dpi))
            print(f"已保存: {out_file} ({pix.width}x{pix.height} px)")

            # 释放资源
            pix = None
            img.close()

    finally:
        doc.close()

    print(f"\n导出完成！共{num_pages}页，输出目录: {output_dir}")


if __name__ == "__main__":
    import sys

    # 拖入文件或命令行参数
    if len(sys.argv) != 2:
        pdf_path = input("请拖入 PDF 文件到终端窗口里，并回车:\n").strip().strip('"').strip("'")
    else:
        pdf_path = sys.argv[1].strip().strip('"').strip("'")

    pdf_path = os.path.normpath(pdf_path)
    if not os.path.isfile(pdf_path):
        print(f"文件不存在: {pdf_path}")
        input("按回车退出...")
        sys.exit(1)

    export_pdf_to_jpg(pdf_path, target_dpi=300, quality=95)
    input("完成，按回车退出...")
