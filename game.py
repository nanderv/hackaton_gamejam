
from gamestate import GameState, merge_two_dicts, reset_game_state
import pyglet
source1 = pyglet.media.load("city.wav")
source2 = pyglet.media.load("forest.wav")
source3 = pyglet.media.load("hell.wav")

__author__ = 'nander'
#/usr/bin/env python
REVIVAL = True
import os
SCALE = 2
import pyglet
#frametime
FT = 1/30
os.sys.path.insert(0, '.')



import sys
import os


FULLSCREEN = False
if FULLSCREEN:
    window = pyglet.window.Window(fullscreen=True)
    wwidth =int(window.width / SCALE)
    hheight =int(window.height / SCALE)
    window.close()
    window = pyglet.window.Window(fullscreen=True,width = wwidth, height = hheight)
else:
    window = pyglet.window.Window()
SOUND_DEMO = True

from player import Player
from json_map import Map
from special_effects import *
pyglet.resource.path = ['assets/tiles','assets/tiles', 'assets/tiles/fence', '', 'Map_Modules', '/assets/entity/player/walking', '/assets/entity/player/standing', 'assets/backgrounds', 'assets/sounds',]
print(pyglet.resource.path)
FULLSCREEN = False


def queue_song(aa=0):
    print ("queueing phase")
    gamestate = GameState.get_instance()
    if gamestate.hippieness > 150*gamestate.musiclevel:
        print("plusplus")
        gamestate.music_player.eos_action = gamestate.music_player.EOS_NEXT
        gamestate.music_player.next()
        gamestate.musiclevel += 1
        gamestate.hippieness += 150

        gamestate.music_player.eos_action = gamestate.music_player.EOS_LOOP
    else:
        print("loop")
        gamestate.music_player.eos_action = gamestate.music_player.EOS_LOOP

    pyglet.clock.schedule_once(queue_song, gamestate.current_source.duration)


@window.event
def update(dt):
    gamestate = GameState.get_instance()
    if gamestate.game_state == "G":
        gamestate.window.clear()
        gamestate.effect_manager = EffectManager()
        gamestate.player.handle_input()
        gamestate.effect_manager.run_effects()
        gamestate.be_hippy()

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

        if gamestate.game_state =="DD":
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





def start_map(map):

    # load the map
    gamestate = GameState.get_instance()
    fd = pyglet.resource.file(map, 'rt')
    gamestate.map = Map.load_json(fd)
    m = gamestate.map

    # set the viewport to the window dimensions
    m.set_viewport(0, 0, window.width, window.height)
    gamestate.hippieness = 31-0

    og_keys = m.objectgroups.keys()
    effect_manager = EffectManager()
    gamestate.effect_manager = effect_manager
    player = None
    testlayer = None

    gamestate.music_player.queue(source1)
    gamestate.music_player.queue(source2)
    gamestate.music_player.queue(source3)
    gamestate.musiclevel = 1
    gamestate.music_player.eos_action = gamestate.music_player.EOS_LOOP
    gamestate.current_source = source1
    gamestate.music_player[1].play()
    gamestate.music_player[2].play()
    gamestate.music_player[3].play()
    print(gamestate.current_source.duration)
    print(gamestate.current_source.duration-2)
    pyglet.clock.schedule_once(queue_song, gamestate.current_source.duration-2)
    tl_keys = m.tilelayers.keys()
    gamestate.all_layers = merge_two_dicts(gamestate.map.tilelayers, gamestate.map.objectgroups)
    for key in og_keys:
        for object in  m.objectgroups[key].objects:
            if str.lower(object["name"]) == "player":
                player = Player(object, m.objectgroups[key], gamestate.keyboardhandler,  m, window)
    gamestate.player = player
    for key in og_keys:
        for object in m.objectgroups[key].objects:
            a = Phase_In(object, 1/FT)
            effect_manager.add_effect(a)
    gamestate.hide_false_layers()



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
