import cv2
import torch
import pytesseract

# YOLO 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'custom', path='/content/drive/MyDrive/yolov5_license/runs/train/geonho_yms02_yolo6/weights/best.pt', force_reload=True)

# 동영상 파일 경로
video_path = "/content/fall.mp4"
output_video_path = "/content/license_plate_detected_video.mp4"
detected_texts_path = "/content/detected_texts.txt"

# 동영상 읽기
cap = cv2.VideoCapture(video_path)

# 동영상 저장 설정
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 저장 코덱 설정
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

# 텍스트 저장 파일 초기화
with open(detected_texts_path, 'w') as f:
    f.write("Detected Texts:\n")

# 프레임 간격 설정 (예: 5 프레임마다 처리)
frame_interval = 3
frame_count = 0

# 프레임 단위로 처리
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 프레임 간격에 따라 처리
    if frame_count % frame_interval == 0:
        # YOLO로 번호판 탐지
        results = model(frame)
        plates = results.pandas().xyxy[0]  # bounding box 좌표 가져오기

        # 번호판 인식 및 OCR 적용
        for i, plate in plates.iterrows():
            x_min, y_min, x_max, y_max = int(plate['xmin']), int(plate['ymin']), int(plate['xmax']), int(plate['ymax'])

            # 번호판 영역 자르기
            plate_img = frame[y_min:y_max, x_min:x_max]

            # 전처리 (흑백 변환)
            gray_plate_img = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)

            # OCR 적용
            text = pytesseract.image_to_string(gray_plate_img, config='--psm 8')  # psm 8은 단일 라인 인식

            # "ECARGUY" 문자열이 포함된 경우에만 출력 및 bounding box 교체
            if "CARGUY" in text.strip():
                print("Detected Plate Text:", text.strip())

                # 텍스트 파일에 저장
                with open(detected_texts_path, 'a') as f:
                    f.write(text.strip() + "\n")

                # 원본 프레임에 bounding box와 OCR 결과 추가
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)  # bounding box
                cv2.putText(frame, text.strip(), (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 결과 프레임 저장
    out.write(frame)
    frame_count += 1

# 자원 해제
cap.release()
out.release()


print(f"Detection result video saved at {output_video_path}")
print(f"Detected texts saved at {detected_texts_path}")
