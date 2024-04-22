import cv2
import threading
from queue import Queue
import time
from ultralytics import YOLO


class ThreadProcess(threading.Thread):
    def __init__(self, capture_queue: Queue, process_queue: Queue):
        super().__init__()
        self.thread_running = False
        self.capture_queue = capture_queue
        self.process_queue = process_queue

        # load model detect or tracking
        self.load_model()

    def load_model(self):
        # load model here
        # example
        self.model = YOLO('resources/weights/yolov8n.pt', task="detect")

    def run(self):
        print("Start processing")
        self.thread_running = True
        while self.thread_running:
            if self.capture_queue.empty():
                time.sleep(0.001)
                continue
            frame = self.capture_queue.get()
            frame_copy = frame.copy()
            # process frame
            results = self.model.predict(frame, imgsz=320, verbose=False)
            # get bounding box
            if not results:
                continue
            result = results[0]
            boxes = result.boxes.xyxy
            if self.process_queue.empty():
                self.process_queue.put([frame_copy, boxes])
            time.sleep(0.001)  # 1ms

    def stop(self):
        self.thread_running = False
        print("Stop processing")
