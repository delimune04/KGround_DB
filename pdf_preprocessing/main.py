import os
import cv2
import numpy as np
from pdf2image import convert_from_path
from multiprocessing import Pool, cpu_count
from PIL import Image
from detect_table import detect_tables_in_image
from extract_table import extract_tables_from_pdf

if __name__ == '__main__':
    input_directory = input("PDF 결과물 폴더 경로를 복사 후 입력하세요: ")
    output_directory = input("결과를 저장할 폴더 경로를 복사 후 입력하세요: ")

    input_directory = os.path.normpath(input_directory)
    output_directory = os.path.normpath(output_directory)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory, exist_ok=True)

    pdf_files = [
        f for f in os.listdir(input_directory) if f.lower().endswith(".pdf")
    ]

    available_cpus = cpu_count()
    print(f"현재 컴퓨터의 CPU 개수는 {available_cpus}개 입니다.")

    num_processes = input("결과 처리에 사용할 CPU 수를 입력하세요 (전체 CPU의 절반 이하 권장): ")

    try:
        num_processes = int(num_processes)
        if num_processes < 1:
            raise ValueError
        if num_processes > available_cpus:
            print(f"입력한 CPU 수가 사용 가능한 CPU 수({available_cpus})보다 많습니다. 최대 사용 가능한 CPU 수로 설정합니다.")
            num_processes = available_cpus
    except ValueError:
        print(f"유효하지 않은 입력입니다. 사용 가능한 CPU 수({available_cpus})로 설정합니다.")
        num_processes = available_cpus

    # 멀티프로세싱
    with Pool(processes=num_processes) as pool:
        args = [(pdf_file, input_directory, output_directory) for pdf_file in pdf_files]
        pool.map(extract_tables_from_pdf, args)