import os
import cv2
import numpy as np
from pdf2image import convert_from_path
from multiprocessing import Pool, cpu_count
from PIL import Image
from detect_table import detect_tables_in_image
from extract_table import extract_tables_from_pdf

if __name__ == '__main__':
    input_directory = r"C:\Users\sp040\OneDrive\바탕 화면\OCR_Test\OCR_pre"  # 입력 PDF 파일들이 있는 디렉토리
    output_directory = r"C:\Users\sp040\OneDrive\바탕 화면\OCR_Test\Result"  # 결과를 저장할 디렉토리

    if not os.path.exists(output_directory):
        os.makedirs(output_directory, exist_ok=True)

    pdf_files = [
        f for f in os.listdir(input_directory) if f.lower().endswith(".pdf")
    ]

    # 멀티프로세싱
    num_processes = 4
    with Pool(processes=num_processes) as pool:
        args = [(pdf_file, input_directory, output_directory) for pdf_file in pdf_files]
        pool.map(extract_tables_from_pdf, args)
