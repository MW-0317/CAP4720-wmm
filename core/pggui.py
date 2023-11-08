from typing import Callable, Annotated

import pygame as pg
import pygame_gui as pggui

from core.Interval import Frame

"""
GUI using Pygame Gui
Author: Mark Williams
--------------------
This will need to be rewritten soon, there's too much rewritting of previously written code.
"""

class UIElement (pggui.core.UIElement):
    shown = False
    def __init__(self, manager):
        # List of events of event type and callback function for event
        self.events: list[list[int, Callable]] = []
        self.manager = manager

    def add_event(self, event_type, callback: Callable):
        self.events.append([event_type, callback])

    def run_event(self, current_event):
        for event in self.events:
            if current_event.type == event[0] and current_event.ui_element == self:
                event[1]()

    def toggle_visibility(self):
        self.shown = not self.shown
        self.show() if self.shown else self.hide()

class Window (UIElement, pggui.elements.UIWindow):
    def __init__(self, manager, *args, **kwargs):
        UIElement.__init__(self, manager)
        pggui.elements.UIWindow.__init__(self, *args, **kwargs)

    def create_element(self, *args, anchor="", classType: type[UIElement] = UIElement, **kwargs):
        anchors = {anchor: anchor}
        element = classType(self.manager, *args, container=self, anchors=anchors, **kwargs)
        self.manager.ui_elements.append(element)
        return element

    def create_button(self, *args, callback: Callable = None, **kwargs):
        button = self.create_element(*args, classType=Button, **kwargs)
        button.add_event(pggui.UI_BUTTON_PRESSED, callback)
        return button
    
    def create_label(self, *args, **kwargs):
        return self.create_element(*args, **kwargs, classType=Label)

    def create_text(self, *args, **kwargs):
        return self.create_element(*args, **kwargs, classType=Text)
    
    def create_window(self, *args, **kwargs):
        window = Window(self.manager, *args, **kwargs)
        return window

class Button (UIElement, pggui.elements.UIButton):
    def __init__(self, manager, *args, **kwargs):
        UIElement.__init__(self, manager)
        pggui.elements.UIButton.__init__(self, *args, **kwargs)

class Label (UIElement, pggui.elements.UILabel):
    def __init__(self, manager, *args, **kwargs):
        UIElement.__init__(self, manager)
        pggui.elements.UILabel.__init__(self, *args, **kwargs)

class Text (UIElement, pggui.elements.UITextBox):
    def __init__(self, manager, *args, **kwargs):
        UIElement.__init__(self, manager)
        pggui.elements.UITextBox.__init__(self, *args, **kwargs)

class guiManager(pggui.UIManager):
    def __init__(self, width, height, surface):
        self.manager = self
        self.width                          = width
        self.height                         = height
        self.ui_elements: list[UIElement]   = []
        self.surface                        = surface
        pggui.UIManager.__init__(self, (width, height), theme_path="./resources/gui/theme.json")

    def create_element(self, *args, anchor="", classType: type[UIElement] = UIElement, **kwargs):
        anchors = {anchor: anchor}
        element = classType(self.manager, *args, anchors=anchors, **kwargs)
        self.manager.ui_elements.append(element)
        return element

    def create_button(self, *args, callback: Callable = None, **kwargs):
        button = self.create_element(*args, classType=Button, **kwargs)
        button.add_event(pggui.UI_BUTTON_PRESSED, callback)
        return button
    
    def create_label(self, *args, **kwargs):
        return self.create_element(*args, **kwargs, classType=Label)

    def create_text(self, *args, **kwargs):
        return self.create_element(*args, **kwargs, classType=Text)
    
    def create_window(self, *args, **kwargs):
        window = Window(self.manager, *args, **kwargs)
        return window
    
    # game.guiManager.queryConfirmation(f"Would you like to buy ${gamestate.properties[property_index][...]}", confirm_callback)
    def query_confirmation(self, text, width, height, callback: Callable = None):
        window_rect = pg.Rect(self.width // 2 - width // 2, self.height // 2 - height // 2, width, height)
        window = self.create_window(rect=window_rect)
        #window.create_text(10, 10, width - 10, height - 10, text="TEST", anchor="center")
        width = width - 30
        height = height - 30
        #window.create_button(40, 40, width - 80, height - 80, text="", anchor="center", callback=callback)
        confirm_rect = pg.Rect(-100 - 20, height - 30 - 20, 100, 30)
        window.create_button(confirm_rect, text="Confirm", anchor="right", callback=callback)
    
    def run_event(self, current_event):
        for element in self.ui_elements:
            element.run_event(current_event)
        
        self.process_events(current_event)

    def process_events(self, event):
        super().process_events(event)

    def frame_update(self, frame: Frame) -> Frame:
        self.update(frame.deltatime)
        self.draw(frame)
        return frame

    def draw(self, frame: Frame):
        self.draw_ui(self.surface)
