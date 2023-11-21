from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import core.Interval as Interval, core.Object as Object

import pyrr

import core.Camera as Camera

class Scene:
    color: pyrr.Vector3 = pyrr.Vector3([0.25, 0.25, 0.25])
    def __init__(self):
        self.objects: list[Object.Object] = []
        self.current_camera: Camera.Camera = None

    def delete(self):
        for obj in self.objects:
            obj.delete()

    def enable(self):
        ...

    def frame_update(self, frame: Interval.Frame) -> Interval.Frame:
        frame.set_scene(self)
        for obj in self.objects:
            if isinstance(obj, Camera.Camera):
                self.current_camera = obj

        frame = self.current_camera.frame_update(frame)
        
        for obj in self.objects:
            if not isinstance(obj, Camera.Camera):
                obj.frame_update(frame)
        
        return frame

    def tick_update(self, tick: Interval.Tick) -> Interval.Tick:
        return tick

    def add_object(self, object):
        self.objects.append(object)