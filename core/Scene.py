from core.Camera import *
from core.Object import Object
from core.Interval import *

class Scene:
    def __init__(self):
        self.objects: list[Object] = []

    def frame_update(self, frame: Frame):
        for object in self.objects:
            if isinstance(object, Camera):
                object.frame_update(frame)
            object.draw()

    def tick_update(self, tick: Tick):
        pass

    def add_object(self, object):
        self.objects.append(object)