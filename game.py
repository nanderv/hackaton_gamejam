from gamestate import GameState

__author__ = 'nander'
#/usr/bin/env python

import os
SCALE = 2
import pyglet
#frametime
FT = 1/60
os.sys.path.insert(0, '.')
from player import Player
from json_map import Map
from special_effects import *
pyglet.resource.path = ['assets/tiles','assets/tiles', 'assets/tiles/fence', '', 'Map_Modules', '/assets/entity/player/walking', '/assets/entity/player/standing', '/assets/entity/player/jumping']
FULLSCREEN = False
if FULLSCREEN:
    window = pyglet.window.Window(fullscreen=True)
    wwidth =int(window.width / SCALE)
    hheight =int(window.height / SCALE)
    window.close()
    window = pyglet.window.Window(fullscreen=True,width = wwidth, height = hheight)
else:
    window = pyglet.window.Window()
gamestate = GameState.get_instance()
gamestate.window = window




@window.event
def update(dt):
    gamestate = GameState.get_instance()
    gamestate.window.clear()
    gamestate.effect_manager = EffectManager()
    gamestate.player.handle_input()
    gamestate.effect_manager.run_effects()
    gamestate.map.draw()
    gamestate.hippieness +=1
    gamestate.be_hippy()

    gamestate.hippieness = max(0, gamestate.hippieness)

def start_map(map):
    # load the map
    gamestate = GameState.get_instance()
    gamestate.layer_setup = {"slow": [300, 500, False]}
    fd = pyglet.resource.file(map, 'rt')
    gamestate.map = Map.load_json(fd)
    m = gamestate.map

    # set the viewport to the window dimensions
    m.set_viewport(0, 0, window.width, window.height)

    # perform some queries to the map data!

    # get the object named "Door1"
    keyboardhandler = pyglet.window.key.KeyStateHandler()
    window.push_handlers(keyboardhandler)
    # get the object in coords (5, 3)
    og_keys = m.objectgroups.keys()
    effect_manager = EffectManager()
    gamestate.effect_manager = effect_manager
    player = None
    testlayer = None
    tl_keys = m.tilelayers.keys()

    for key in og_keys:
        for object in  m.objectgroups[key].objects:
            if str.lower(object["name"]) == "player":
                player =Player(object, m.objectgroups[key], keyboardhandler, m, window)
    gamestate.player = player
    for key in og_keys:
        for object in m.objectgroups[key].objects:
            a = Phase_In(object, 1/FT)
            effect_manager.add_effect(a)
    gamestate.hide_false_layers()
    pyglet.clock.schedule_interval(update, FT)

    pyglet.app.run()
start_map("city_nander_test.json")
