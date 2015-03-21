__author__ = 'nander'
#/usr/bin/env python

import pyglet
import os
os.sys.path.insert(0, '.')

from json_map import Map

window = pyglet.window.Window(fullscreen=True)
window.set_vsync(0)
# load the map
fd = pyglet.resource.file("test.json", 'rt')
m = Map.load_json(fd)


# set the viewport to the window dimensions
m.set_viewport(0, 0, window.width, window.height)

# perform some queries to the map data!

# get the object named "Door1"
keyboardhandler = pyglet.window.key.KeyStateHandler()
window.push_handlers(keyboardhandler)
# get the object in coords (5, 3)
@window.event
def update(dt):
    og_keys = m.objectgroups.keys()
    for key in og_keys:
        for object in m.objectgroups[key].objects:
            d_x = 0
            d_y = 0
            if keyboardhandler[pyglet.window.key.D]:
                d_x += 1
            if keyboardhandler[pyglet.window.key.A]:
                d_x += -1
            if keyboardhandler[pyglet.window.key.S]:
                d_y += 1
            if keyboardhandler[pyglet.window.key.W]:
                d_y += -1
            m.objectgroups[key].move(object, d_x, d_y)
            object["rotation"] += 1
    window.clear()
    m.invalidate()
    m.move_focus(1, 0)
    m.draw()

print(m.tilelayers["collision"][10, 10])
pyglet.clock.schedule_interval(update, 1.0/60.0)
pyglet.clock.set_fps_limit(60)
pyglet.app.run()