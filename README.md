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

```


