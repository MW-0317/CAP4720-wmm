from typing import Callable, Annotated

import pygame as pg
import pygame_gui as pggui

from core.Interval import Frame, Tick

"""
GUI using Pygame Gui
Author: Mark Williams
--------------------
Still need to write
    - Card Animation
    - Dice on screen
    - Money gained "+(num)" next to money count
"""

class UIElement (pggui.core.UIElement):
    shown = False
    should_remove = False
    container = None
    def __init__(self, manager):
        # List of events of event type and callback function for event
        self.events: list[list[int, Callable]] = []
        self.manager = manager

    def add_event(self, event_type, callback: Callable):
        self.events.append([event_type, callback])

    def run_event(self, current_event):
        for event in self.events:
            if current_event.type == event[0] and current_event.ui_element == self:
                event[1](self)

    def toggle_visibility(self):
        self.shown = not self.shown
        self.show() if self.shown else self.hide()

    def get_super_container(self):
        return self.container
    
    def tick(self, tick: Tick):
        return tick

class ElementHolder:
    def get_container(self):
        return self

    def create_element(self, *args, anchor="", classType: type[UIElement] = UIElement, **kwargs):
        anchors = {anchor: anchor}
        element = classType(self.manager, *args, container=self.get_container(), anchors=anchors, **kwargs)
        element.container = self.get_container()
        self.manager.ui_elements.append(element)
        return element
    
    def create_button(self, *args, callback: Callable = lambda ui: None, **kwargs):
        button = self.create_element(*args, classType=Button, **kwargs)
        button.add_event(pggui.UI_BUTTON_PRESSED, callback)
        return button
    
    def create_label(self, *args, **kwargs):
        return self.create_element(*args, **kwargs, classType=Label)
    
    def create_update_label(self, *args, **kwargs):
        return self.create_element(*args, **kwargs, classType=UpdateLabel)

    def create_text(self, *args, **kwargs):
        return self.create_element(*args, **kwargs, classType=Text)
    
    def create_image(self, filename, *args, **kwargs):
        return self.create_element(filename, *args, **kwargs, classType=Image)
    
class Window (UIElement, pggui.elements.UIWindow, ElementHolder):
    def __init__(self, manager, *args, **kwargs):
        UIElement.__init__(self, manager)
        pggui.elements.UIWindow.__init__(self, *args, **kwargs)

class Button (UIElement, pggui.elements.UIButton):
    def __init__(self, manager, *args, **kwargs):
        UIElement.__init__(self, manager)
        pggui.elements.UIButton.__init__(self, *args, **kwargs)

class Label (UIElement, pggui.elements.UILabel):
    def __init__(self, manager, *args, **kwargs):
        UIElement.__init__(self, manager)
        pggui.elements.UILabel.__init__(self, *args, **kwargs)

class Image (UIElement, pggui.elements.UIImage):
    def __init__(self, manager, filename, *args, **kwargs):
        surface = pg.image.load(filename)
        UIElement.__init__(self, manager)
        pggui.elements.UIImage.__init__(self, image_surface=surface, *args, **kwargs)

class UpdateLabel (UIElement, pggui.elements.UILabel):
    def __init__(self, manager, *args, **kwargs):
        UIElement.__init__(self, manager)
        pggui.elements.UILabel.__init__(self, *args, **kwargs)

        #self.opacity = 0

    def tick(self, tick: Tick):
        #self.opacity -= 1
        return tick

    def update_value(self, text):
        self.opacity = 100
        self.set_text(text)

class Text (UIElement, pggui.elements.UITextBox):
    def __init__(self, manager, *args, **kwargs):
        UIElement.__init__(self, manager)
        pggui.elements.UITextBox.__init__(self, *args, **kwargs)

class guiManager(pggui.UIManager, ElementHolder):
    def __init__(self, width, height, surface):
        self.manager = self
        self.width                          = width
        self.height                         = height
        self.ui_elements: list[UIElement]   = []
        self.ui_queue                       = []
        self.window_active                  = False
        self.surface                        = surface
        pggui.UIManager.__init__(self, (width, height), theme_path="./resources/gui/theme.json")
        self._load_fonts()

        self.current_select: UIElement = None

    def _load_fonts(self):
        fonts = [{'name': 'fira_code', 'point_size': 18, 'style': 'regular'}]
        self.preload_fonts(fonts)

    def get_container(self):
        return None
    
    def create_window(self, *args, **kwargs):
        window = Window(self.manager, *args, **kwargs)
        return window
    
    def query_window(self, text, width, height, offset=0, *args, **kwargs):
        self.window_active = True
        window_rect = pg.Rect(self.width // 2 - width // 2 + offset, self.height // 2 - height // 2, width, height)
        window = self.create_window(rect=window_rect)

        width = width - 30
        height = height - 30

        text_size = (width - width // 15, height - height // 3)
        text_rect = pg.Rect(width // 2 - text_size[0] // 2, height // 15, text_size[0], text_size[1])
        window.create_text(relative_rect=text_rect, html_text=text)
        self.ui_queue.append(window)

        return window, width, height
    
    def query_image(self, filename, width, height, offset=0, *args, **kwargs):
        image_rect = pg.Rect(self.width // 2 - width // 2 - offset, self.height // 2 - height // 2, width, height)
        image = self.create_image(filename, relative_rect=image_rect)

        width = width - 30
        height = height - 30

        self.ui_queue.append(image)

        return image, width, height
    
    def query_image_select(self, filenames, width, height, *args, i = 0, **kwargs):
        def next(isright):
            if isright: 
                self.query_image_select(filenames, width, height, *args, i=(i+1) % len(filenames), **kwargs)
            else:
                self.query_image_select(filenames, width, height, *args, i=(i-1) % len(filenames), **kwargs)
        window, wWidth, wHeight = self.query_confirmation("", width * 1.2, height * 1.8, confirm_text="Right", decline_text="Left", callback=next)
        window.create_image(filenames[i], relative_rect=pg.Rect(wWidth // 2 - width // 2, wHeight // 2 - height // 1.5, width, height))
        self.current_select = window
        self.current_option = filenames[i]
    
    def query_option(self, text, width, height, first_option="One", second_option="Two", callback: Callable = lambda ui: None):
        ...
    
    def query_confirmation(self, text, width, height, confirm_text="Confirm", decline_text="Decline", callback: Callable = lambda ui: None, offset=0):
        window, width, height = self.query_window(text, width, height, offset)

        def close_window_and_callback(ui_element, confimed: bool):
            self.window_active = False
            window.kill()
            callback(confimed)

        confirm_id = pggui.core.ObjectID("@query_button", "#confirm_button")
        confirm_size = (width // 2.7, height // 8)
        confirm_rect = pg.Rect(-confirm_size[0] - width // 15, height - confirm_size[1] - height // 15, confirm_size[0], confirm_size[1])
        window.create_button(confirm_rect, text=confirm_text, anchor="right", callback=lambda ui_element: close_window_and_callback(ui_element, True), object_id=confirm_id)

        decline_id = pggui.core.ObjectID("@query_button", "#decline_button")
        decline_size = (width // 2.7, height // 8)
        decline_rect = pg.Rect(width // 15, height - confirm_size[1] - height // 15, confirm_size[0], confirm_size[1])
        window.create_button(decline_rect, text=decline_text, anchor="left", callback=lambda ui_element: close_window_and_callback(ui_element, False), object_id=decline_id)
        return window, width, height
    
    def query_message(self, text, width, height, okay_text="Okay", callback: Callable = lambda ui: None):
        window, width, height = self.query_window(text, width, height)

        def close_window(ui_element):
            self.window_active = False
            window.kill()
            callback(ui_element)

        okay_id = pggui.core.ObjectID("@query_button", "")
        okay_size = (width // 2.7, height // 8)
        okay_rect = pg.Rect((width // 2 - okay_size[0] // 2, height - okay_size[1] - height // 15), okay_size)
        window.create_button(okay_rect, text=okay_text, callback=close_window)

    def run_event(self, current_event):
        # Elements are yet to be removed when killed TODO
        elements_size = len(self.ui_elements)
        i = 0
        while i < elements_size:
            element = self.ui_elements[i]
            element.run_event(current_event)
            i+=1
        
        self.process_events(current_event)

    def process_events(self, event):
        super().process_events(event)
    
    def process_queue(self):
        ...

    def frame_update(self, frame: Frame) -> Frame:
        self.process_queue()
        self.update(frame.deltatime)
        self.draw(frame)
        return frame
    
    def tick_update(self, tick: Tick) -> Tick:
        for ui in self.ui_elements:
            ui.tick(tick)
        return tick

    def draw(self, frame: Frame):
        self.draw_ui(self.surface)
