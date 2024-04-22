from ultralytics import YOLO
import cv2

# Model yolov8
model = YOLO('yolov8n.pt')

# Image
im = cv2.imread('zidane.jpg')

results = model.predict(im, imgsz=320)
result = results[0]
# get bounding box
boxes = result.boxes.xyxy

for box in boxes:
    print(box)
    x1, y1, x2, y2 = list(map(int, box))
    cv2.rectangle(im, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imshow('image', im)
cv2.waitKey(0)
