import yaml
from .camera_controller import CameraController
from typing import List


class MainController(object):
    def __init__(self):
        super().__init__()
        # load camera
        self.cameras_config = {}
        self.load_camera()

        # load stream config
        self.stream_config = {}
        self.load_stream()

        # create camera
        self.list_camera: List[CameraController] = []
        self.create_camera()

    def load_camera(self):
        with open('resources/config/camera.yml') as f:
            self.cameras_config = yaml.load(f, Loader=yaml.FullLoader)

    def load_stream(self):
        with open('resources/config/stream.yml') as f:
            self.stream_config = yaml.load(f, Loader=yaml.FullLoader)

    def create_camera(self):
        for key, value in self.cameras_config.items():
            camera_id = key
            camera_url = value["url"]
            camera = CameraController(
                camera_id, camera_url, self.stream_config["url"])
            self.list_camera.append(camera)

    def start(self):
        print("Start all camera: ", len(self.list_camera))
        for camera in self.list_camera:
            camera.start()

    def stop(self):
        for camera in self.list_camera:
            camera.stop()
