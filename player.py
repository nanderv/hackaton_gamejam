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
        vx = 0
        vy = 0
        jump = False
        if self.keyboardhandler[pyglet.window.key.D]:
            vx = 1
        if self.keyboardhandler[pyglet.window.key.A]:
            vx = -1
        if self.keyboardhandler[pyglet.window.key.S]:
            vy = -1
        if self.keyboardhandler[pyglet.window.key.W]:
            vy = 1
        if self.keyboardhandler[pyglet.window.key.SPACE]:
            jump = True

        self.object["jump"] = jump
        self.object["vy"] = vy
        self.object["vx"] = vx
        self.objectgroup.move(self.object)