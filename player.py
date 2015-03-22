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
            vy -= 1
        if (self.keyboardhandler[pyglet.window.key.W] or
                self.keyboardhandler[pyglet.window.key.UP]):
            vy += 1
            idle = False
            portal = True
        if self.keyboardhandler[pyglet.window.key.SPACE]:
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
        print(self.playerState)
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
        self.add_animation("walk_left","assets/entity/player/walking_hflip/walking_hflip.png" , 10)
        self.add_animation("jumping_right","assets/entity/player/jumping/jumping.png" , 10)
        self.add_animation("jumping_left","assets/entity/player/jumping_hflip/jumping_hflip.png" , 10)


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
