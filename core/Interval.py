from core.Camera import *
from core.Scene import *

class Interval:
    def __init__(self, deltatime):
        self.deltatime = deltatime
        self.camera: Camera
        self.scene: Scene

class Frame(Interval):
    def __init__(self, deltatime):
        super().__init__(deltatime)

class Tick(Interval):
    def __init__(self, deltatime):
        super().__init__(deltatime)