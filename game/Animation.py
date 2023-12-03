from __future__ import annotations
from typing import Callable

from core.Object import Object
from core.Interval import Tick
import pyrr

class Keyframe:
    # Length in ticks
    def __init__(self, value: pyrr.Vector3, length):
        self.value = value
        self.length = length

class Animation:
    def movement(self, fromValue, toValue, time, keyframes):
        fromValue = pyrr.Vector3(fromValue)
        toValue   = pyrr.Vector3(toValue)

        start = Keyframe(fromValue, time)
        end = Keyframe(toValue, 0)

        keyframes.append(start)
        keyframes.append(end)

    def translation(self, posFrom, posTo, time):
        self.movement(posFrom, posTo, time, self.positions)

    def rotation(self, rotFrom, rotTo, time):
        self.movement(rotFrom, rotTo, time, self.rotations)

    def scale(self, scaleFrom, scaleTo, time):
        self.movement(scaleFrom, scaleTo, time, self.scales)

    def __init__(self, anim_object: Object):
        self.anim_object: Object = anim_object
        self.total_ticks = 0

        self.positions: list[Keyframe]  = []
        self.last_position_tick         = 0
        self.scales:    list[Keyframe]  = []
        self.last_scale_tick            = 0
        self.rotations: list[Keyframe]  = []
        self.last_rotation_tick         = 0

    def animate(self, tick: Tick, keyframes: list[Keyframe], last_tick, set_callback: Callable):
        if keyframes == []: return

        length = keyframes[0].length
        next_tick = last_tick + length

        if length == 0:
            set_callback(keyframes.pop(0).value)
            return
        
        if self.total_ticks > next_tick:
            keyframes.pop(0)
            set_callback(keyframes[0].value)
            return

        valueTo     = keyframes[1].value
        valueFrom   = keyframes[0].value

        #print(valueTo)
        #print(valueFrom)

        #partial = valueFrom + (valueTo - valueFrom) * ((maxtime - starttime) / (time-starttime))
        partial = ((self.total_ticks - last_tick) / length) * (valueTo) + (1 - (self.total_ticks - last_tick) / length) * (valueFrom)
        #print(partial)

        set_callback(partial)
    
    def is_empty(self):
        return self.positions == [] and self.scales == [] and self.rotations == []

    def tick_update(self, tick: Tick):
        self.animate(tick, self.positions, self.last_position_tick, self.anim_object.set_position)
        self.animate(tick, self.scales, self.last_scale_tick, self.anim_object.set_scale)
        self.animate(tick, self.rotations, self.last_rotation_tick, self.anim_object.set_rotation)
        self.total_ticks += 1