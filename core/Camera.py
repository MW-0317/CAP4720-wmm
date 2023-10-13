from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import core.Interval as Interval

import core.Object as Object

import pyrr, math, datetime

class Camera(Object.Object):
    def __init__(self, position: list[float, float, float], fov: int, aspect: float):
        self.position   = pyrr.Vector3(position)
        self.fov        = fov
        self.aspect     = aspect
        self.tilt       = 0
        self.pan        = 0
        self.up         = pyrr.Vector3([0, 1, 0])
        self.right      = pyrr.Vector3([1, 0, 0])
        self.forward    = pyrr.Vector3([0, 0, -1])
        self.vbo = None
        self.vao = None

    def frame_update(self, frame: Interval.Frame) -> Interval.Frame:
        frame.set_camera(self)
        return frame

    def tick_update(self, tick: Interval.Tick) -> Interval.Tick:
        return tick

    def get_view_matrix(self) -> pyrr.Matrix44:
        rotX = pyrr.matrix44.create_from_x_rotation(math.radians(self.tilt))
        rotY = pyrr.matrix44.create_from_y_rotation(math.radians(self.pan))
        newForward = pyrr.matrix44.apply_to_vector(rotX, self.forward)
        newForward = pyrr.matrix44.apply_to_vector(rotY, newForward)
        view = pyrr.matrix44.create_look_at(self.position, self.position + newForward, self.up)
        return view

    def get_projection_matrix(self):
        return pyrr.matrix44.create_perspective_projection_matrix(self.fov, self.aspect, 0.1, 1000)

    def set_fov(self, fov: int):
        self.fov = fov

    def set_aspect(self, aspect: float):
        self.aspect = aspect