import cv2
import torch
import pytesseract

# YOLO 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'custom', path='/content/drive/MyDrive/yolov5_license/runs/train/geonho_yms02_yolo6/weights/best.pt', force_reload=True)

# 이미지 파일 경로
image_path = "/content/caraa.jpg"
output_path = "/content/license_plate_detected.jpg"

# 이미지 로드
image = cv2.imread(image_path)

# YOLO로 번호판 탐지
results = model(image)
plates = results.pandas().xyxy[0]  # bounding box 좌표 가져오기

# 번호판 인식 및 OCR 적용
for i, plate in plates.iterrows():
    x_min, y_min, x_max, y_max = int(plate['xmin']), int(plate['ymin']), int(plate['xmax']), int(plate['ymax'])

    # 번호판 영역 자르기
    plate_img = image[y_min:y_max, x_min:x_max]

    # 전처리 (흑백 변환)
    gray_plate_img = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)

    # OCR 적용
    text = pytesseract.image_to_string(gray_plate_img, config='--psm 8')  # psm 8은 단일 라인 인식
    print("Detected Plate Text:", text.strip())

    # 원본 이미지에 bounding box와 OCR 결과 추가
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)  # bounding box
    cv2.putText(image, text.strip(), (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# 결과 저장
cv2.imwrite(output_path, image)
print(f"Detection result saved at {output_path}")
