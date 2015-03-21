from pyglet.gl import glScalef, glTexParameteri, GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST, GL_TEXTURE_MAG_FILTER
from special_effects import Phase_In, EffectManager
from player import fancy_move_cam
from hackaton_gamejam.Map_Modules.gamestate import GameState

__author__ = 'nander'
#/usr/bin/env python

import os

import pyglet
#frametime
FT = 1/60
os.sys.path.insert(0, '.')
from player import Player
from json_map import Map
from special_effects import *
pyglet.resource.path = ['assets/tiles','assets/tiles', 'assets/tiles/fence', '', 'Map_Modules', '/assets/entity/player/walking', '/assets/entity/player/standing', '/assets/entity/player/jumping']

window = pyglet.window.Window(fullscreen=False, width = 800, height = 600)
window.set_vsync(0)
gamestate = GameState.get_instance()
gamestate.window = window
@window.event
def update(dt):
    gamestate = GameState.get_instance()
    gamestate.window.clear()

    gamestate.player.handle_input()
    gamestate.effect_manager.run_effects()
    gamestate.map.draw()

def start_map(map):
    # load the map
    gamestate = GameState.get_instance()
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


    pyglet.clock.schedule_interval(update, FT)
    pyglet.clock.set_fps_limit(1/FT)
    pyglet.app.run()
start_map("testmaplong.json")
