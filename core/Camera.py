from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import core.Interval as Interval

import core.Object as Object

import pyrr, math

class Camera(Object.Object):
    def __init__(self, position: list[float, float, float], fov: int, aspect: float):
        self.position   = position
        self.fov        = fov
        self.aspect     = aspect
        self.tilt       = 0
        self.pan        = 0
        self.up         = [0, 1, 0]
        self.right      = [0, 0, 1]
        self.forward    = [1, 0, 0]

    def frame_update(self, frame: Interval.Frame) -> Interval.Frame:
        #rotX = pyrr.matrix44.create_from_x_rotation(math.radians(self.tilt))
        #rotY = pyrr.matrix44.create_from_y_rotation(math.radians(self.pan))
        #pyrr.matrix44.apply_to_vector(rotX, )

        frame.set_camera(self)
        return frame

    def tick_update(self):
        ...

    def get_view_matrix(self) -> pyrr.Matrix44:
        view = pyrr.matrix44.create_look_at(self.position, [0, 0, 0], self.up)
        view = pyrr.matrix44.multiply(view, pyrr.matrix44.create_from_translation(-1 * pyrr.Vector3(self.position)))
        return view

    def get_projection_matrix(self):
        return pyrr.matrix44.create_perspective_projection_matrix(self.fov, self.aspect, 0.1, 1000)

    def set_fov(self, fov: int):
        self.fov = fov

    def set_aspect(self, aspect: float):
        self.aspect = aspect