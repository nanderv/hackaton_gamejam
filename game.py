from gamestate import GameState, merge_two_dicts, reset_game_state
import pyglet

source1 = pyglet.media.load("city.wav")
source2 = pyglet.media.load("forest.wav")
source3 = pyglet.media.load("hell.wav")

# source0 = pyglet.media.load("jump.wav", streaming=False)
# source1 = pyglet.media.load("pill.wav", streaming=False)
# source2 = pyglet.media.load("bounce.wav", streaming=False)
# source1 = pyglet.media.load("city.wav")
source0 = pyglet.media.load("forest.wav")
# source3 = pyglet.media.load("hell.wav")

__author__ = 'nander'
# /usr/bin/env python
REVIVAL = False
import os

SCALE = 2
import pyglet
#frametime
FT = 1 / 30
os.sys.path.insert(0, '.')

import sys
import os


FULLSCREEN = True
if FULLSCREEN:
    window = pyglet.window.Window(fullscreen=True)
    wwidth = int(window.width / SCALE)
    hheight = int(window.height / SCALE)
    window.close()
    window = pyglet.window.Window(fullscreen=True, width=wwidth, height=hheight)
else:
    window = pyglet.window.Window()
SOUND_DEMO = True

from player import Player
from json_map import Map
from special_effects import *

pyglet.resource.path = ['assets/tiles', 'assets/tiles', 'assets/tiles/fence', '', 'Map_Modules',
                        '/assets/entity/player/walking', '/assets/entity/player/standing', 'assets/backgrounds',
                        'assets/sounds', ]

print(pyglet.resource.path)
FULLSCREEN = False
music_number = 1


def start_music():
    gamestate = GameState.get_instance()
    # gamestate.music_player.push_handlers(on_eos=catch_eos)
    gamestate.music_player.eos_action = gamestate.music_player.EOS_LOOP
    gamestate.music_player.queue(source0)
    # gamestate.music_player.queue(source1)
    # gamestate.music_player.queue(source2)
    gamestate.music_player.play()


# gamestate.music_player.next()

# gamestate.music_player.queue(source0)
# gamestate.music_player.queue(source0)
# gamestate.music_player.queue(source0)
# gamestate.music_player.queue(source0)



def catch_eos():
    print("meuk!!!")
    gamestate = GameState.get_instance()
    global music_number
    # gamestate.music_player.pop_handlers()
    # gamestate.music_player.push_handlers(on_eos=catch_eos)
    print(gamestate.hippieness, music_number)
    if gamestate.hippieness <= 40 and music_number == 1:
        pass
    elif gamestate.hippieness >= 50 and music_number == 1:
        gamestate.music_player.next()
        music_number = 2
    elif gamestate.hippieness >= 60 and music_number == 2:
        gamestate.music_player.next()
        music_number = 3
    else:
        pass
    #gamestate.music_player.play()


@window.event
def update(dt):

    << << << < HEAD
gamestate = GameState.get_instance()
if gamestate.game_state == "G":
    gamestate.window.clear()
    gamestate.effect_manager = EffectManager()
    gamestate.player.handle_input()
    gamestate.effect_manager.run_effects()
    gamestate.be_hippy()

    gamestate.run_ai()
    gamestate.map.draw()
else:
    if gamestate.game_state == "D":
        print("You are DEAD")
        gamestate.game_state = "DDD"
    if gamestate.game_state == "DDD":
        if gamestate.keyboardhandler[pyglet.window.key.SPACE]:
            if REVIVAL:
                gamestate.game_state = "G"
            else:
                gamestate.game_state = "DD"

    if gamestate.game_state == "DD":
        keyboardhandler = gamestate.keyboardhandler
        window = gamestate.window
        window.push_handlers()

        for layer in gamestate.map.objectgroups.values():
            layer.delete_sprites()
        for layer in gamestate.map.tilelayers.values():
            layer.delete_sprites()

        del gamestate.map.batch
        del gamestate.map.batch2
        del gamestate.map.batch3

        del gamestate.player
        del gamestate.map.data
        del gamestate.map.tilesets
        del gamestate.map.objectgroups
        del gamestate.map

        del gamestate

        gamestate = reset_game_state()
        gamestate.window = window

        start_map("CityForest2.json")

        if keyboardhandler[pyglet.window.key.SPACE]:
            start_map("CityForest.json")
            gamestate.game_state = "L"

    if gamestate.game_state == "L":
        gamestate.game_state = "G"


== == == =
gamestate = GameState.get_instance()
if gamestate.game_state == "G":
    gamestate.window.clear()
    gamestate.effect_manager = EffectManager()
    gamestate.player.handle_input()
    gamestate.effect_manager.run_effects()
    gamestate.be_hippy()

    gamestate.run_ai()
    gamestate.map.draw()
else:
    if gamestate.game_state == "D":
        print("You are DEAD")
        gamestate.game_state = "DDD"
    if gamestate.game_state == "DDD":
        if gamestate.keyboardhandler[pyglet.window.key.SPACE]:
            if REVIVAL:
                gamestate.game_state = "G"
            else:
                gamestate.game_state = "DD"

    if gamestate.game_state == "DD":
        keyboardhandler = gamestate.keyboardhandler
        window = gamestate.window
        window.push_handlers()

        for layer in gamestate.map.objectgroups.values():
            layer.delete_sprites()
        for layer in gamestate.map.tilelayers.values():
            layer.delete_sprites()

        del gamestate.map.batch
        del gamestate.map.batch2
        del gamestate.map.batch3

        del gamestate.player
        del gamestate.map.data
        del gamestate.map.tilesets
        del gamestate.map.objectgroups
        del gamestate.map

        del gamestate

        gamestate = reset_game_state()
        gamestate.window = window

        start_map("CityForest2.json")

        if keyboardhandler[pyglet.window.key.SPACE]:
            start_map("CityForest.json")
            gamestate.game_state = "L"

    if gamestate.game_state == "L":
        print("loaded your game")
        gamestate.game_state = "G"
>> >> >> > 60
bf5078a15fdd0d5dfea7eeaf77dd7e87fe29da


def start_map(map):
    # load the map
    gamestate = GameState.get_instance()
    fd = pyglet.resource.file(map, 'rt')
    gamestate.map = Map.load_json(fd)
    m = gamestate.map

    # set the viewport to the window dimensions
    m.set_viewport(0, 0, window.width, window.height)
    gamestate.hippieness = 31 - 0

    og_keys = m.objectgroups.keys()
    effect_manager = EffectManager()
    gamestate.effect_manager = effect_manager
    player = None
    testlayer = None
    start_music()
    tl_keys = m.tilelayers.keys()
    gamestate.all_layers = merge_two_dicts(gamestate.map.tilelayers, gamestate.map.objectgroups)
    for key in og_keys:
        for object in m.objectgroups[key].objects:
            if str.lower(object["name"]) == "player":
                player = Player(object, m.objectgroups[key], gamestate.keyboardhandler, m, window)
    gamestate.player = player
    for key in og_keys:
        for object in m.objectgroups[key].objects:
            a = Phase_In(object, 1 / FT)
            effect_manager.add_effect(a)
    gamestate.hide_false_layers


og_keys = m.objectgroups.keys()
effect_manager = EffectManager()
gamestate.effect_manager = effect_manager
player = None
testlayer = None


<< << << < HEAD
gamestate.music_player.queue(source1)
gamestate.music_player.queue(source2)
gamestate.music_player.queue(source3)
gamestate.musiclevel = 1
gamestate.music_player.eos_action = gamestate.music_player.EOS_LOOP
gamestate.current_source = source1
#gamestate.music_player[1].play()
#gamestate.music_player[2].play()
#gamestate.music_player[3].play()
#   pyglet.clock.schedule_once(queue_song, gamestate.current_source.duration-2)
tl_keys = m.tilelayers.keys()
gamestate.all_layers = merge_two_dicts(gamestate.map.tilelayers, gamestate.map.objectgroups)
for key in og_keys:
    for object in m.objectgroups[key].objects:
        if str.lower(object["name"]) == "player":
            player = Player(object, m.objectgroups[key], gamestate.keyboardhandler, m, window)
gamestate.player = player
for key in og_keys:
    for object in m.objectgroups[key].objects:
        a = Phase_In(object, 1 / FT)
        effect_manager.add_effect(a)
gamestate.hide_false_layers()

== == == =
>> >> >> > 60
bf5078a15fdd0d5dfea7eeaf77dd7e87fe29da


def start_game():
    gamestate = GameState.get_instance()
    gamestate.window = window
    keyboardhandler = pyglet.window.key.KeyStateHandler()
    window.push_handlers(keyboardhandler)

    gamestate.keyboardhandler = keyboardhandler
    start_map("CityForest.json")
    pyglet.clock.schedule_interval_soft(update, FT)
    pyglet.app.run()


start_game()
