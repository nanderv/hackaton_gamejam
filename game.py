__author__ = 'nander'
#/usr/bin/env python

import os

import pyglet

os.sys.path.insert(0, '.')
from player import Player
from json_map import Map
from special_effects import *

window = pyglet.window.Window(fullscreen=False)
window.set_vsync(0)
# load the map
pyglet.resource.path = [ 'tiles','']
fd = pyglet.resource.file("test.json", 'rt')
m = Map.load_json(fd)


# set the viewport to the window dimensions
m.set_viewport(0, 0, window.width, window.height)

# perform some queries to the map data!

# get the object named "Door1"
keyboardhandler = pyglet.window.key.KeyStateHandler()
window.push_handlers(keyboardhandler)
# get the object in coords (5, 3)
og_keys = m.objectgroups.keys()
effect_manager  = EffectManager()
player = None
testlayer = None
tl_keys = m.tilelayers.keys()
if "testlayer" in tl_keys:
    testlayer = m.tilelayers["testlayer"]

for key in og_keys:
    for object in  m.objectgroups[key].objects:
        if object["name"] == "player":
            player =Player(object, m.objectgroups[key], keyboardhandler)


for key in og_keys:
    for object in m.objectgroups[key].objects:
        a = Phase_In(object, 60)
        effect_manager.add_effect(a)
@window.event
def update(dt):
    player.handle_input()
    effect_manager.run_effects()
    if testlayer is not None:
        testlayer.set_opacity(128)
    object["rotation"] += 1
    window.clear()
    m.move_focus(1, 0)
    m.draw()

print(m.tilelayers["collision"][10, 10])
pyglet.clock.schedule_interval(update, 1.0/60.0)
pyglet.clock.set_fps_limit(60)
pyglet.app.run()