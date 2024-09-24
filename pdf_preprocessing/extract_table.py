import os
from pdf2image import convert_from_path
from detect_table import detect_tables_in_image

def extract_tables_from_pdf(args):
    pdf_file, input_directory, output_directory, poppler_path = args

    pdf_path = os.path.join(input_directory, pdf_file)
    try:
        images = convert_from_path(pdf_path, poppler_path=poppler_path)
    except Exception as e:
        print(f"{pdf_file} 처리 중 오류 발생: {e}")
        return

    for i, image in enumerate(images):
        try:
            print(f"{pdf_file} - {i+1} 페이지를 처리 중입니다...")
            tables = detect_tables_in_image(image)
            if tables:
                for idx, table in enumerate(tables):
                    table_image_path = os.path.join(
                        output_directory,
                        f"{os.path.splitext(pdf_file)[0]}_page{i+1}_table{idx+1}.png"
                    )
                    table.save(table_image_path)
            else:
                print(f"{pdf_file} - {i+1} 페이지에서 테이블을 찾을 수 없습니다.")
        except Exception as e:
            print(f"{pdf_file} - {i+1} 페이지 처리 중 오류 발생: {e}")