from gamestate import GameState, merge_two_dicts

__author__ = 'nander'
#/usr/bin/env python

import os
SCALE = 2
import pyglet
#frametime
FT = 1/30
os.sys.path.insert(0, '.')



import sys
import os
def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)




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
keyboardhandler = pyglet.window.key.KeyStateHandler()
window.push_handlers(keyboardhandler)
gamestate.keyboardhandler = keyboardhandler



@window.event
def update(dt):
    gamestate = GameState.get_instance()
    if gamestate.game_state == "G":
        gamestate.window.clear()
        gamestate.effect_manager = EffectManager()
        gamestate.player.handle_input()
        gamestate.effect_manager.run_effects()
        gamestate.hippieness +=0.2
        gamestate.hippieness = max(0, gamestate.hippieness)
        gamestate.be_hippy()
        gamestate.map.draw()
    else:
        if gamestate.game_state == "D":
            print("You are DEAD")

            if gamestate.keyboardhandler[pyglet.window.key.SPACE]:

                gamestate.game_state = "DD"
        if gamestate.game_state =="DD":
            start_map("CityForest.json")
            gamestate.game_state = "G"

        if gamestate.game_state == "L":
            print("loaded your game")
            gamestate.game_state = "G"




def start_map(map):
    # load the map
    gamestate = GameState.get_instance()
    fd = pyglet.resource.file(map, 'rt')
    gamestate.map = Map.load_json(fd)
    m = gamestate.map
    fps_display = pyglet.clock.ClockDisplay()
    fps_display.draw()
    # set the viewport to the window dimensions
    m.set_viewport(0, 0, window.width, window.height)

    # perform some queries to the map data!

    # get the object named "Door1"

    # get the object in coords (5, 3)
    og_keys = m.objectgroups.keys()
    effect_manager = EffectManager()
    gamestate.effect_manager = effect_manager
    player = None
    testlayer = None
    tl_keys = m.tilelayers.keys()
    gamestate.all_layers = merge_two_dicts(gamestate.map.tilelayers, gamestate.map.objectgroups)
    for key in og_keys:
        for object in  m.objectgroups[key].objects:
            if str.lower(object["name"]) == "player":
                player = Player(object, m.objectgroups[key], keyboardhandler, m, window)
    gamestate.player = player
    for key in og_keys:
        for object in m.objectgroups[key].objects:
            a = Phase_In(object, 1/FT)
            effect_manager.add_effect(a)
    gamestate.hide_false_layers()

start_map("CityForest.json")
pyglet.clock.schedule_interval(update, FT)
pyglet.app.run()