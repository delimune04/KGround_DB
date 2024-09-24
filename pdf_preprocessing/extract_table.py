import os
import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
from detect_table import detect_tables_in_image
from PyPDF2 import PdfReader  # 추가된 부분


def extract_tables_from_pdf(pdf_file, input_directory, output_directory):
    input_pdf_path = os.path.join(input_directory, pdf_file)
    output_pdf_name = os.path.splitext(os.path.basename(pdf_file))[0] + '_tables.pdf'
    output_pdf_path = os.path.join(output_directory, output_pdf_name)

    table_images = []

    try:
        # PDF의 총 페이지 수를 얻어옵니다.
        reader = PdfReader(input_pdf_path)
        num_pages = len(reader.pages)

        for page_number in range(num_pages):
            try:
                #print(f"{pdf_file} - {page_number + 1} 페이지를 처리 중입니다...")

                # 페이지를 한 장씩 이미지로 변환합니다.
                images = convert_from_path(
                    input_pdf_path, dpi=150, first_page=page_number + 1, last_page=page_number + 1
                )
                if not images:
                    #print(f"{pdf_file} - {page_number + 1} 페이지를 변환하지 못했습니다.")
                    continue

                image = images[0]

                # PIL 이미지를 OpenCV 이미지로 변환 (복사 최소화)
                img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

                # 표 영역 검출
                table_regions = detect_tables_in_image(img_cv)
                #print(f"{pdf_file} - {page_number + 1} 페이지에서 {len(table_regions)}개의 표를 검출했습니다.")

                if not table_regions:
                    continue

                for idx, (x, y, w, h) in enumerate(table_regions):
                    table_img_cv = img_cv[y:y+h, x:x+w]

                    # OpenCV 이미지를 PIL 이미지로 변환
                    table_img_pil = Image.fromarray(cv2.cvtColor(table_img_cv, cv2.COLOR_BGR2RGB))

                    table_images.append(table_img_pil)
                    #print(f"표 이미지를 리스트에 추가했습니다: 페이지 {page_number + 1}, 표 {idx + 1}")

                # 메모리 해제
                del image
                del img_cv
                del table_img_cv
                del images

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
