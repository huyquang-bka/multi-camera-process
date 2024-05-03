import threading
from queue import Queue
import subprocess
import time
import cv2


class ThreadStream(threading.Thread):
    def __init__(self, stream_queue: Queue, stream_url: str, camera_id: int, stream_size: list = [640, 480]):
        super().__init__()
        self.thread_running = False
        self.thread_running = False
        self.stream_queue = stream_queue
        self.stream_size = stream_size
        self.stream_args = (
            "ffmpeg -r 15 -re -stream_loop -1 -f rawvideo -vcodec rawvideo -pix_fmt "
            f"rgb24 -s {stream_size[0]}x{stream_size[1]} -i pipe:0 -pix_fmt yuv420p -c:v libx264 -preset ultrafast -b:v 8196k  "
            f"-f rtsp {stream_url}/{camera_id} ").split()
        self.pipe = subprocess.Popen(self.stream_args, stdin=subprocess.PIPE)
        print(f"Stream at: {stream_url}/{camera_id}")

    def run(self):
        print("Start streaming")
        self.thread_running = True
        while self.thread_running:
            if self.stream_queue.empty():
                time.sleep(0.001)
                continue
            frame, bboxes = self.stream_queue.get()
            for bbox in bboxes:
                x1, y1, x2, y2 = list(map(int, bbox))
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            if frame.shape[:2] != self.stream_size[::-1]:
                frame = cv2.resize(frame, tuple(self.stream_size))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            try:
                self.pipe.stdin.write(frame.tobytes())
            except Exception as e:
                print("Error stream: ", e)
                self.pipe = subprocess.Popen(
                    self.stream_args, stdin=subprocess.PIPE)
        print("Stop streaming")

    def stop(self):
        self.thread_running = False
        print("Stop streaming")
