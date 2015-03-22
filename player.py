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
        self.animation_object = object["sprite"]
        self.window = window
        self.sprite = self.object["sprite"]

    def handle_input(self):
        vx = self.object["vx"]

        vy = self.object["vy"]

        jump = False
        idle = True
        if (self.keyboardhandler[pyglet.window.key.D] or
                self.keyboardhandler[pyglet.window.key.RIGHT]) and self.object["ax"] == 0:
                if self.playerState is not "walk_right":
                    self.animation_object.set_animation("walk_right")
                    self.playerState="walk_right"
                idle = False
                vx += 1
        if (self.keyboardhandler[pyglet.window.key.A] or
                self.keyboardhandler[pyglet.window.key.LEFT]) and self.object["ax"] == 0:
                if self.playerState is not "walk_left":
                    self.animation_object.set_animation("walk_left")
                    self.playerState="walk_left"
                idle= False
                vx -= 1
        if (self.keyboardhandler[pyglet.window.key.S] or
                self.keyboardhandler[pyglet.window.key.DOWN]) and self.object["ay"] == 0:
            vy -= 1
            idle = False

        if (self.keyboardhandler[pyglet.window.key.W] or
                self.keyboardhandler[pyglet.window.key.UP]) and self.object["ay"] == 0:
            vy += 1
            idle = False
        if self.keyboardhandler[pyglet.window.key.SPACE]:
            jump = True
            idle = False

        if idle:
                if self.playerState is not "idle":
                    self.animation_object.set_animation("idle")
                    self.playerState="idle"

        self.object["jump"] = jump
        self.object["vy"] = vy
        self.object["vx"] = vx


        self.objectgroup.move(self.object)
        fancy_move_cam(self.object, self.map, self.window)


class AnimatedObject(pyglet.sprite.Sprite):
    default = None
    animations = {}

    def __init__(self, default,dx,dy,dbatch,dgroup,dusage, length):
        raw = pyglet.resource.image(default)

        raw_seq = pyglet.image.ImageGrid(raw, 1, length)
        self.default = pyglet.image.Animation.from_image_sequence(raw_seq, 1/6, True)
        pyglet.sprite.Sprite.__init__(self, self.default,x=dx,
                                        y=dy,
                                        batch=dbatch,
                                        group=dgroup,
                                        usage=dusage)

    def set_animation(self, name):
        self.image = self.animations.get(name, self.default)


    def add_animation(self, name, default, length):
        raw = pyglet.resource.image(default)
        raw_seq = pyglet.image.ImageGrid(raw, 1, length)
        animation = pyglet.image.Animation.from_image_sequence(raw_seq, 1/30)

        self.animations[name] = animation

    def onTick(self):
        pass

class PlayerAnimatedObject(AnimatedObject):

    def __init__(self,x,y,batch,group,usage):
        AnimatedObject.__init__(self, "assets/entity/player/standing/standing.png",x,y,batch,group,usage, 10)
        self.add_animation("walk_right","assets/entity/player/walking/walking.png" , 10)
        self.add_animation("jumping","assets/entity/player/jumping/jumping.png" , 10)

class GooseObject(AnimatedObject):

    def __init__(self,x,y,batch,group,usage):
        AnimatedObject.__init__(self, "assets/entity/sprite_goose.png",x,y,batch,group,usage, 6)


class BulletObject(AnimatedObject):

    def __init__(self, x, y, batch, group, usage, vx, vy):
        super().__init__(self, "assets/entity/sprite_pink_elephant.png", x, y, batch, group, usage, 10)
        self.vx = vx
        self.vy = vy

    def onTick(self):
        super().onTick()
        self.x += self.vx
        self.y += self.vy

def fancy_move_cam(object, map, window):


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

    if win_max_x+camX < objX:
        res_x = objX - win_max_x

    if win_min_y + res_y > objY:
        res_y = objY - win_min_y

    if win_max_y + res_y < objY:
         res_y = objY - win_max_y

    map.set_viewport(res_x, res_y, map.w, map.h)
