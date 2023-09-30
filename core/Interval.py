from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import core.Camera as Camera, core.Scene as Scene

class Interval:
    def __init__(self, deltatime):
        self.deltatime = deltatime
        self.camera: Camera.Camera = None
        self.scene: Scene.Scene = None

    def set_camera(self, camera: Camera.Camera):
        self.camera = camera

    def set_scene(self, scene: Scene.Scene):
        self.scene = scene

class Frame(Interval):
    def __init__(self, deltatime):
        super().__init__(deltatime)

class Tick(Interval):
    def __init__(self, deltatime):
        super().__init__(deltatime)