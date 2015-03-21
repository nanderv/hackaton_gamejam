__author__ = 'nander'
import pyglet

class Player():
    object = None
    objectgroup = None
    keyboardhandler = None
    def __init__(self, object, objectgroup, keyboardhandler):
        self.object = object
        self.keyboardhandler = keyboardhandler
        self.objectgroup = objectgroup

    def handle_input(self):
            d_x = 0
            d_y = 0
            if self.keyboardhandler[pyglet.window.key.D]:
                d_x += 1
            if self.keyboardhandler[pyglet.window.key.A]:
                d_x += -1
            if self.keyboardhandler[pyglet.window.key.S]:
                d_y += -1
            if self.keyboardhandler[pyglet.window.key.W]:
                d_y += 1
            self.objectgroup.move(self.object, d_x, d_y)
