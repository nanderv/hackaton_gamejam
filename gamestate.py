import pyglet
from special_effects import FadeLayerIn, FadeLayerOut, EffectManager, Phase_In

__author__ = 'nander'
from player import Player

def reset_game_state():
    gamestate= GameState.get_instance()
    gamestate.game_state = "L"
    gamestate.INSTANCE = None
    gamestate.FT = 1/60
    gamestate.current_map = "CityForest.json"
    gamestate.hippieness = 60
    gamestate.layer_setup = {}
    gamestate.UPSCALE = 2
    gamestate.window = None
    gamestate.all_layers={}
    gamestate.ai_list = []
    gamestate.func = None
    gamestate.enabled_collision_layers = []
    gamestate.enabled_death_layers = []
    gamestate.enabled_climb_layers = []

    return gamestate

class GameState():
    #D: Death, M: Menu, G: Game, C: Credits

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = GameState()
        player = pyglet.media.Player()
        return cls.INSTANCE

    @classmethod
    def reset_instance(cls):
        cls.INSTANCE = GameState()
        return cls.INSTANCE
    game_state = "L"
    INSTANCE = None
    FT = 1/60

    current_map = "CityForest.json"
    hippieness = 0
    music_player = None
    layer_setup = {}
    UPSCALE = 2
    window = None
    all_layers={}
    ai_list = []
    func = None
    enabled_collision_layers = []
    enabled_death_layers = []
    enabled_climb_layers = []

    def start_game(self):
        game_state = "L"
    def add_load_function(self, func):
        self.func = func

    def run_ai(self):
        for ai in self.ai_list:
            ai.ai()


    def check_layers(self):
        pass

    def be_hippy(self):
            for cs in self.all_layers.values():
                wanted_state  = float(cs.min_hippieness) <= self.hippieness < float(cs.max_hippieness)
                if wanted_state != cs.curVis:
                    if cs.collision_layer:
                        if wanted_state:
                            self.enabled_collision_layers.append(cs)
                        else:
                            if cs in self.enabled_collision_layers:
                                self.enabled_collision_layers.remove(cs)
                    elif cs.death_layer:
                        if wanted_state:
                            self.enabled_death_layers.append(cs)
                        else:
                            if cs in self.enabled_death_layers:
                                self.enabled_death_layers.remove(cs)
                    elif cs.climb_layer:
                        if wanted_state:
                            self.enabled_climb_layers.append(cs)
                        else:
                            if cs in self.enabled_death_layers:
                                self.enabled_climb_layers.remove(cs)
                    if wanted_state:
                        GameState.get_instance().effect_manager.add_effect(FadeLayerIn(cs, 16))
                    else:
                        GameState.get_instance().effect_manager.add_effect(FadeLayerOut(cs, 16))
                    cs.curVis = wanted_state

    def hide_false_layers(self):
            gamestate = GameState.get_instance()
            for cs in gamestate.all_layers.values():
                    if cs.collision_layer:
                        if float(cs.min_hippieness) <= self.hippieness <= float(cs.max_hippieness):
                            self.enabled_collision_layers.append(cs)
                    elif cs.death_layer:
                        if float(cs.min_hippieness) <= self.hippieness <= float(cs.max_hippieness):
                            self.enabled_death_layers.append(cs)
                    elif cs.climb_layer:
                        if float(cs.min_hippieness) <= self.hippieness <= float(cs.max_hippieness):
                            self.enabled_climb_layers.append(cs)
                    else:
                        if  float(cs.min_hippieness) <= self.hippieness <= float(cs.max_hippieness):
                            cs.set_opacity(255)
                            cs.curVis = True
                        else:
                            cs.set_opacity(0)
                            cs.curVis = False
    def tile_collide(self,x,y):
        ret = 0
        for layer in self.enabled_collision_layers:
            ret += layer[x, y]
        return ret
    def tile_death(self,x,y):
        ret = 0
        for layer in self.enabled_death_layers:
            ret += layer[x, y]
        return ret
    def tile_climb(self,x,y):
        ret = 0
        for layer in self.enabled_climb_layers:
            ret += layer[x, y]
        return ret

def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z
