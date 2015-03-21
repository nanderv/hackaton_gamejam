__author__ = 'nander'
import pyglet
import os
camera_slide_window = {"x": 1/4, "y": 1/4, "xmax": 3/4, "ymax": 3/4}
class Player():
    object = None
    objectgroup = None
    keyboardhandler = None
    map = None
    window = None
    playerState = None
    animation_object = None
    def __init__(self, object, objectgroup, keyboardhandler, map, window):
            # walking_anim
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
        fancy_move_cam(self.object, self.map, self.window, mv)


class AnimatedObject(pyglet.sprite.Sprite):
    default = None
    animations = {}

    def __init__(self, default,dx,dy,dbatch,dgroup,dusage):
        raw = pyglet.resource.image(default)

        raw_seq = pyglet.image.ImageGrid(raw, 1, 10)
        self.default = pyglet.image.Animation.from_image_sequence(raw_seq, 0.5, True)
        pyglet.sprite.Sprite.__init__(self, self.default,x=dx,
                                        y=dy,
                                        batch=dbatch,
                                        group=dgroup,
                                        usage=dusage)

    def set_animation(self, name):
        self.image = self.animations.get(name, self.default)


    def add_animation(self, name, default):
        raw = pyglet.resource.image(default)
        raw_seq = pyglet.image.ImageGrid(raw, 1, 7)
        animation = pyglet.image.Animation.from_image_sequence(raw_seq, 60)

        self.animations[name] = animation

class PlayerAnimatedObject(AnimatedObject):

    def __init__(self,x,y,batch,group,usage):
        AnimatedObject.__init__(self, "assets/entity/player/standing/standing.png",x,y,batch,group,usage)
        self.add_animation("walking","assets/entity/player/walking/walking.png" )
        self.add_animation("jumping","assets/entity/player/jumping/jumping.png" )


def fancy_move_cam(object, map, window, mv):

    d_x = mv[0]
    d_y = mv[1]

    if "sprite" not in object.keys():
        return
    camX = map.x
    camY = map.y

    objX = object["x"]
    objY = object["y"]
    win_min_x = camera_slide_window["x"]*window.width
    win_min_y = camera_slide_window["y"]*window.width
    win_max_x = camera_slide_window["xmax"]*window.width
    win_max_y = camera_slide_window["ymax"]*window.height
    res_x = camX
    res_y = camY
    if win_min_x+res_x > objX:
        res_x = objX - win_min_x
        print("moved left")

    if win_max_x+camX < objX:
        res_x = objX - win_max_x
        print("moved right")

    if win_min_y + res_y > objY:
        res_y = objY - win_min_y
        print("moved up")

    if win_max_y + res_y < objY:
         res_y = objY - win_max_y
         print("moved down")

    map.set_viewport(res_x, res_y, map.w, map.h)