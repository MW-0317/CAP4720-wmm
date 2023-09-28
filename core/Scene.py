from core.Object import Object

class Scene:
    def __init__(self):
        self.objects: list[Object] = []

    def frame_update(self):
        for object in self.objects:
            object.draw()

    def tick_update(self):
        pass

    def add_object(self, object):
        self.objects.append(object)