from queue import Queue
from ..threads import *
from threading import Thread
from typing import List


class CameraController(object):
    def __init__(self, camera_id: int, camera_url: str, stream_url: str) -> None:
        super().__init__()
        self.camera_id = camera_id
        self.camera_url = camera_url
        self.stream_url = stream_url

        self.list_thread: List[Thread] = []

        self.create_queue()
        self.create_thread()

    def create_queue(self):
        self.capture_queue = Queue()
        self.process_queue = Queue()

    def create_thread(self):
        self.thread_capture = ThreadCapture(
            self.camera_url, self.capture_queue)
        self.thread_process = ThreadProcess(
            self.capture_queue, self.process_queue)
        self.thread_stream = ThreadStream(
            self.process_queue, self.stream_url, self.camera_id)

        self.list_thread = [self.thread_capture,
                            self.thread_process, self.thread_stream]

    def start(self):
        print("Start camera: ", self.camera_id)
        for thread in self.list_thread:
            thread.start()

    def stop(self):
        for thread in self.list_thread:
            thread.stop()
