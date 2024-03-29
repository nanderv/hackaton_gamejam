from concurrent.futures import thread
import threading
import time

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
    statechanged = False
    def __init__(self, object, objectgroup, keyboardhandler, map, window):
            # walking_anim
        self.object = object
        self.keyboardhandler = keyboardhandler
        self.objectgroup = objectgroup
        self.map = map

        self.animation_object = object["sprite"]
        self.window = window
        self.sprite = self.object["sprite"]

    state_importance = {"jumping_left": 2, "jumping_right": 2, "walking_left": 1, "walking_right":1, "idle":0}
    def set_animation_state(self):
        if self.prev_animation is not self.playerState:
            self.animation_object.set_animation(self.playerState)

    def add_animation_state(self,state):
        if self.playerState is None:
            self.playerState = state
        elif self.state_importance.get(state,-1) > self.state_importance.get(self.playerState,-1):
            self.playerState = state
        self.statechanged = True

    up = False
    def handle_input(self):
        self.prev_animation = self.playerState
        self.playerState = None
        self.statechanged = False


        vx = self.object["vx"]
        portal = self.object["portal"]
        vy = self.object["vy"]

        jump = False
        idle = True
        if (self.keyboardhandler[pyglet.window.key.D] or
                self.keyboardhandler[pyglet.window.key.RIGHT]):
                self.add_animation_state("walk_right")
                vx += 1



        if (self.keyboardhandler[pyglet.window.key.A] or
                self.keyboardhandler[pyglet.window.key.LEFT]):
            vx -= 1
            self.add_animation_state("walk_left")
        if (self.keyboardhandler[pyglet.window.key.S] or
                self.keyboardhandler[pyglet.window.key.DOWN]):
            if self.object["climb"]:
                vy = -1
        if (self.keyboardhandler[pyglet.window.key.W] or
                self.keyboardhandler[pyglet.window.key.UP]):
            idle = False
            if self.object["climb"]:
                vy =1
            portal = True


        if self.keyboardhandler[pyglet.window.key.SPACE]:


            up = True
            jump = True

            idle = False
            if self.playerState == "walk_left":
                self.add_animation_state("jumping_left")
            else:
                self.add_animation_state("jumping_right")


        if not self.statechanged:
                    self.playerState = "idle"

        self.set_animation_state()

        self.object["jump"] = jump
        self.object["vy"] = vy
        self.object["vx"] = vx
        self.object["portal"] = portal
        self.objectgroup.move(self.object)
        fancy_move_cam(self.object, self.map, self.window)
        self.joystick_input = []



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
        self.add_animation("walk_left","assets/entity/player/walking_hflip/walking_hflip.png" , 10)
        self.add_animation("jumping_right","assets/entity/player/jumping/jumping.png" , 10)
        self.add_animation("jumping_left","assets/entity/player/jumping_hflip/jumping_hflip.png" , 10)


class Roaming_Monster(AnimatedObject):
    pos = 0
    max = 64
    dir = 1
    baseX = 0
    animation1 = None
    animation2 = None
    def __init__(self,animation, x,y,batch,group,usage, frames, max):
        self.max = max
        self.baseX = x
        AnimatedObject.__init__(self, animation,x,y,batch,group,usage, frames)

    def ai(self):
        self.pos = self.pos + self.dir
        self.object["x"] += self.dir
        if self.pos <= 0 or self.pos == self.max:
            self.dir *= -1
            self.set_animation(self.dir)
        self.x = self.baseX + self.pos

class Vertical_Roaming_Monster(AnimatedObject):
    animation1 = None
    animation2 = None
    pos = 0
    max = 64
    dir = 1
    baseY = 0
    def __init__(self,animation, x,y,batch,group,usage, frames, max):
        self.max = max
        self.baseY = y
        AnimatedObject.__init__(self, animation,x,y,batch,group,usage, frames)
    def ai(self):
        self.pos += self.dir
        self.object["y"] += self.dir
        if self.pos <= 0 or self.pos == self.max:
            self.dir *= -1
            self.set_animation(self.dir)
        self.y = self.baseY - self.pos


class GooseObject(Roaming_Monster):

    def __init__(self,x,y,batch,group,usage):

        Roaming_Monster.__init__(self, "assets/entity/sprite_goose.png",x,y,batch,group,usage, 6,(2*32))
        self.add_animation("a", "assets/entity/sprite_goose.png" ,6)
        self.add_animation("b", "assets/entity/sprite_goose_hflip.png" ,6)

class DevilObject(Roaming_Monster):
    def __init__(self,x,y,batch,group,usage):
        Roaming_Monster.__init__(self, "assets/entity/sprite_devil.png",x,y,batch,group,usage, 10,(4*32))
        self.add_animation("c", "assets/entity/sprite_devil.png",10)
        self.add_animation("d", "assets/entity/sprite_devil_hflip.png",10)

class EvilGooseObject(Vertical_Roaming_Monster):
    def __init__(self,x,y,batch,group,usage):
        Roaming_Monster.__init__(self, "assets/entity/sprite_evil_goose.png",x,y,batch,group,usage, 6,(2*32))
        self.add_animation("e", "assets/entity/sprite_evil_goose.png" ,6)
        self.add_animation("f", "assets/entity/sprite_evil_goose_hflip.png" ,6)

class HedgehogObject(Roaming_Monster):
    def __init__(self,x,y,batch,group,usage):
        Roaming_Monster.__init__(self, "assets/entity/hedgehog.png",x,y,batch,group,usage, 4,(2*32))
        self.add_animation("g", "assets/entity/hedgehog.png" ,4)
        self.add_animation("h", "assets/entity/hedgehog_hflip.png" ,4)

class PinkElephantObject(Roaming_Monster):
    def __init__(self,x,y,batch,group,usage):
        Roaming_Monster.__init__(self, "assets/entity/sprite_pink_elephant.png",x,y,batch,group,usage, 10,(3*32))
        self.add_animation("i", "assets/entity/sprite_pink_elephant.png" ,10)
        self.add_animation("j", "assets/entity/sprite_pink_elephant_hflip.png" ,10)

class SawBladeObject(Vertical_Roaming_Monster):
    def __init__(self,x,y,batch,group,usage):
        Roaming_Monster.__init__(self, "assets/entity/sprite_sawblade.png",x,y,batch,group,usage, 8,(4*32))
        self.add_animation("k", "assets/entity/sprite_sawblade.png" ,8)

class TurtleObject(Vertical_Roaming_Monster):
    def __init__(self,x,y,batch,group,usage):
        Roaming_Monster.__init__(self, "assets/entity/sprite_turtle_walking.png",x,y,batch,group,usage, 12,(6*32))
        self.add_animation("l", "assets/entity/sprite_turtle_walking.png" ,12)
        self.add_animation("m", "assets/entity/sprite_turtle_walking_hflip.png",12)

class SkullObject(Roaming_Monster):
    def __init__(self,x,y,batch,group,usage):
        Roaming_Monster.__init__(self, "assets/entity/skull_idle.png",x,y,batch,group,usage, 12,(2*32))
        self.add_animation("n", "assets/entity/skull_idle.png" ,12)


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

