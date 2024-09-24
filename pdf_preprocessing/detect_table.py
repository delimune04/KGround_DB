import cv2

def detect_tables_in_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    table_regions = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # 표로 간주할 만한 크기 조건 설정 (필요에 따라 조정)
        if w > 100 and h > 100:
            table_regions.append((x, y-100, w, h+100))
    return table_regions