## yms_AI
## Detecting fallen people

## download yolov5
```bash
git clone https://github.com/ultralytics/yolov5
cd ./yolov5
!pip install -r requirements.txt
```

## detect video
```bash
# 동영상 파일 경로
source_path = '/path/your/video'

# 모델 가중치 파일 경로
weights_path = "/path/your/weights"

# detect.py 실행
%cd /content/yolov5
!python detect.py --source {source_path} --weights {weights_path}


# 프로젝트 GIF 데모

### 첫 번째 GIF
![첫 번째 GIF](https://raw.githubusercontent.com/Fall-2024-Database-15-5CM/yms_AI/main/KakaoTalk_20241210_153133169.gif)

### 두 번째 GIF
![두 번째 GIF](https://raw.githubusercontent.com/Fall-2024-Database-15-5CM/yms_AI/main/KakaoTalk_20241210_153224897.gif)

### 세 번째 GIF
![세 번째 GIF](https://raw.githubusercontent.com/Fall-2024-Database-15-5CM/yms_AI/main/KakaoTalk_20241213_192002619.gif)


