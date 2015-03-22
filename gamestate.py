from special_effects import FadeLayerIn, FadeLayerOut

__author__ = 'nander'


class GameState():
    INSTANCE = None
    hippieness = 0
    layer_setup = {}
    UPSCALE = 2
    window = None
    all_layers={}
    enabled_collision_layers = []

    def __init__(self):
        if self.INSTANCE is not None:
            raise ValueError("An instantiation already exists!")


            # do your init stuff

    @classmethod
    def get_instance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = GameState()

        return cls.INSTANCE

    def check_layers(self):
        pass

    def be_hippy(self):
            for cs in self.all_layers.values():
                wanted_state  = float(cs.min_hippieness) < self.hippieness < float(cs.max_hippieness)
                if wanted_state != cs.curVis:
                    if cs.collision_layer:
                        if wanted_state:
                            self.enabled_collision_layers.append(cs)
                            #GameState.get_instance().effect_manager.add_effect(FadeLayerIn(cs, 255))
                        else:
                            self.enabled_collision_layers.remove(cs)
                            #GameState.get_instance().effect_manager.add_effect(FadeLayerOut(cs, 255))
                    else:
                        if wanted_state:
                            cs.set_opacity(255)
                            #GameState.get_instance().effect_manager.add_effect(FadeLayerIn(cs, 255))
                        else:
                            cs.set_opacity(0)
                            #GameState.get_instance().effect_manager.add_effect(FadeLayerOut(cs, 255))
                    cs.curVis = wanted_state

    def hide_false_layers(self):
            gamestate = GameState.get_instance()

            for cs in gamestate.all_layers.values():
                    if cs.collision_layer:
                        if float(cs.min_hippieness) <= self.hippieness <= float(cs.max_hippieness):
                            self.enabled_collision_layers.append(cs)
                            #GameState.get_instance().effect_manager.add_effect(FadeLayerIn(cs, 255))
                        else:
                            self.enabled_collision_layers.remove(cs)
                            #GameState.get_instance().effect_manager.add_effect(FadeLayerOut(cs, 255))
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



def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z