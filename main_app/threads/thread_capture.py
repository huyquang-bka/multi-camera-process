import cv2
import threading
from queue import Queue
import time


class ThreadCapture(threading.Thread):
    def __init__(self, camera_url: str, capture_queue: Queue):
        super().__init__()
        self.thread_running = False
        self.camera_url = camera_url
        self.capture_queue = capture_queue

    def run(self):
        print("Start capturing url: ", self.camera_url)
        cap = cv2.VideoCapture(self.camera_url)
        self.thread_running = True
        while self.thread_running:
            ret, frame = cap.read()
            if not ret:
                print("Reconnecting to camera: ", self.camera_url)
                cap = cv2.VideoCapture(self.camera_url)
                time.sleep(1)
                continue
            if self.capture_queue.empty():
                self.capture_queue.put(frame)
            time.sleep(0.03)  # 30ms

    def stop(self):
        self.thread_running = False
        print("Stop capturing url: ", self.camera_url)
