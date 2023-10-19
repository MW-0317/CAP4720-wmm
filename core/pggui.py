from typing import Callable

import pygame as pg
import pygame_gui as pggui

from core.Interval import Frame

class UIElement:
    id = None
    def __init__(self):
        # List of events of event type and callback function for event
        self.events: list[list[int, Callable]] = []

    def add_event(self, event_type, callback: Callable):
        self.events.append([event_type, callback])

    def run_event(self, current_event):
        for event in self.events:
            if current_event.type == event[0] and current_event.ui_element == self.id:
                event[1]()

class Button (UIElement):
    def __init__(self, x, y, width, height, manager, text=None):
        self.id = pggui.elements.UIButton(relative_rect=pg.Rect((x, y), (width, height)),
                                            text=text,
                                            manager=manager)
        super().__init__()

class Text (UIElement):
    def __init__(self, x, y, width, height, mananger, text=None):
        self.id = pggui.elements.UITextBox(text,
                                           relative_rect=pg.Rect((x, y), (width, height)),
                                           manager=mananger)
        super().__init__()

class guiManager:
    def __init__(self, width, height, surface):
        self.width                          = width
        self.height                         = height
        self.manager                        = pggui.UIManager((width, height))
        self.ui_elements: list[UIElement]   = []
        self.surface                        = surface

    def create_button(self, x, y, width, height, text=None, callback: Callable = None):
        button = Button(x, y, width, height, self.manager, text)
        button.add_event(pggui.UI_BUTTON_PRESSED, callback)
        self.ui_elements.append(button)
        return button

    def create_text(self, x, y, width, heigth, text=None):
        text = Text(x, y, width, heigth, self.manager, text)
        self.ui_elements.append(text)
        return text

    def run_event(self, current_event):
        for element in self.ui_elements:
            element.run_event(current_event)
        
        self.process_events(current_event)

    def process_events(self, event):
        self.manager.process_events(event)

    def frame_update(self, frame: Frame) -> Frame:
        self.manager.update(frame.deltatime)
        self.draw(frame)
        return frame

    def draw(self, frame: Frame):
        self.manager.draw_ui(self.surface)
