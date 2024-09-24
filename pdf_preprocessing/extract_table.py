import os
import sys
import cv2
import numpy as np
import fitz  # PyMuPDF
from PIL import Image
from detect_table import detect_tables_in_image

# 실행 파일 내에서 리소스 경로 설정
if getattr(sys, 'frozen', False):
    # PyInstaller에 의해 패키징된 경우
    base_path = sys._MEIPASS
else:
    # 스크립트가 직접 실행되는 경우
    base_path = os.path.dirname(os.path.abspath(__file__))


def extract_tables_from_pdf(pdf_file, input_directory, output_directory):
    input_pdf_path = os.path.join(input_directory, pdf_file)
    output_pdf_name = os.path.splitext(os.path.basename(pdf_file))[0] + '_tables.pdf'
    output_pdf_path = os.path.join(output_directory, output_pdf_name)

    table_images = []

    try:
        # PyMuPDF를 사용하여 PDF의 총 페이지 수를 얻습니다.
        with fitz.open(input_pdf_path) as doc:
            num_pages = doc.page_count

            for page_number in range(num_pages):
                try:
                    # 페이지를 가져옵니다.
                    page = doc.load_page(page_number)
                    # 페이지를 이미지로 변환합니다.
                    pix = page.get_pixmap(dpi=150)
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                    # PIL 이미지를 OpenCV 이미지로 변환
                    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

                    # 표 영역 검출
                    table_regions = detect_tables_in_image(img_cv)

                    if not table_regions:
                        continue

                    for idx, (x, y, w, h) in enumerate(table_regions):
                        table_img_cv = img_cv[y:y + h, x:x + w]

                        # OpenCV 이미지를 PIL 이미지로 변환
                        table_img_pil = Image.fromarray(cv2.cvtColor(table_img_cv, cv2.COLOR_BGR2RGB))

                        table_images.append(table_img_pil)

                except Exception as e:
                    print(f"{pdf_file} - {page_number + 1} 페이지 처리 중 오류 발생: {e}")
                    continue

        if table_images:
            first_image = table_images[0]
            if len(table_images) > 1:
                first_image.save(
                    output_pdf_path, "PDF", resolution=100.0, save_all=True, append_images=table_images[1:]
                )
            else:
                first_image.save(output_pdf_path, "PDF", resolution=100.0)
            print(f"{pdf_file}를 변환 했습니다.: {output_pdf_path}")
        else:
            print(f"{pdf_file}에서 표를 검출하지 못했습니다. 결과 파일이 생성되지 않습니다.")

    except Exception as e:
        print(f"{pdf_file} 처리 중 오류 발생: {e}")
