from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import core.Interval as Interval, core.Object as Object

import core.Camera as Camera

class Scene:
    def __init__(self):
        self.objects: list[Object.Object] = []

    def delete(self):
        for obj in self.objects:
            obj.delete()

    def frame_update(self, frame: Interval.Frame) -> Interval.Frame:
        for obj in self.objects:
            if isinstance(obj, Camera.Camera):
                frame = obj.frame_update(frame)
        
        for obj in self.objects:
            if not isinstance(obj, Camera.Camera):
                obj.draw(frame)
        return frame

    def tick_update(self, tick: Interval.Tick) -> Interval.Tick:
        return tick

    def add_object(self, object):
        self.objects.append(object)