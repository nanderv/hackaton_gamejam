__author__ = 'nander'
from game import *
if FULLSCREEN:
    window = pyglet.window.Window(fullscreen=True)
    wwidth =int(window.width / SCALE)
    hheight =int(window.height / SCALE)
    window.close()
    window = pyglet.window.Window(fullscreen=True,width = wwidth, height = hheight)
else:
    window = pyglet.window.Window()

start_game()

