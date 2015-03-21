from hackaton_gamejam.special_effects import FadeLayerIn, FadeLayerOut

__author__ = 'nander'


class GameState():
    INSTANCE = None
    hippieness = 0
    layer_setup = {}

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
        for layernr in self.layer_setup.keys():
            all_layers = merge_two_dicts(self.map.tilelayers, self.map.objectgroups)
            if layernr in all_layers.keys():
                cs = self.layer_setup[layernr]
                wanted_state = wanted_state = cs[0] < self.hippieness < cs[1]

                if wanted_state != cs[2]:
                    layer = all_layers.get(layernr, None)
                    if wanted_state:
                        GameState.get_instance().effect_manager.add_effect(FadeLayerIn(layer, 120))
                    else:
                        GameState.get_instance().effect_manager.add_effect(FadeLayerOut(layer, 120))
                    self.layer_setup[layernr][2] = wanted_state

    def hide_false_layers(self):
        for layernr in self.layer_setup.keys():
            all_layers = merge_two_dicts(self.map.tilelayers, self.map.objectgroups)
            if layernr in all_layers.keys():
                cs = self.layer_setup[layernr]
                print(self.layer_setup)
                layer = all_layers.get(layernr, None)
                if cs[2]:
                    layer.set_opacity(255)
                else:
                    print("no opacity")
                    layer.set_opacity(0)



def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z