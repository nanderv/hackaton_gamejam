__author__ = 'nander'
import pyglet
camera_slide_window = {"x": 1/4, "y": 1/4, "xmax": 3/4, "ymax": 3/4}
class Player():
    object = None
    objectgroup = None
    keyboardhandler = None
    map = None
    window = None
    def __init__(self, object, objectgroup, keyboardhandler, map, window):
        self.object = object
        self.keyboardhandler = keyboardhandler
        self.objectgroup = objectgroup
        self.map = map
        self.window = window

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
        mv = self.objectgroup.move(self.object)
        fancy_move_cam(self, self.map, self.window, mv)



def fancy_move_cam(player, map, window, mv):
    x = camera_slide_window["x"]*window.width
    d_x = mv[0]
    d_y = mv[1]
    y = camera_slide_window["y"]*window.height
    maxx = camera_slide_window["xmax"]*window.width
    maxy = camera_slide_window["ymax"]*window.height
    if maxx > player.object["sprite"].x > x and maxy > player.object["sprite"].y > y:
        map.move_focus(-d_x, -d_y)