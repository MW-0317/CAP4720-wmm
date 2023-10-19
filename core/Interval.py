from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import core.Camera as Camera, core.Scene as Scene

class Interval:
    def __init__(self):
        self.deltatime                          = None
        self.time                               = None
        self.camera:            Camera.Camera   = None
        self.scene:             Scene.Scene     = None

    def set_camera(self, camera: Camera.Camera):
        self.camera = camera

    def set_scene(self, scene: Scene.Scene):
        self.scene = scene

class Frame(Interval):
    def __init__(self):
        super().__init__()

class Tick(Interval):
    def __init__(self):
        super().__init__()