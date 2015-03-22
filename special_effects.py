__author__ = 'nander'

class Effect ():

    frame = 0
    time = 100
    object = None
    def __init__ (self, object, time):
        self.object = object
        self.time = time

    def run_effect(self):
        self.frame += 1
        if self.frame == self.time:
            return False
        return True

class EffectManager():
    effects = []

    def __init__(self):
        pass

    def add_effect(self, effect):
        self.effects.append(effect)

    def run_effects(self):
        delete_effects = []
        for effect in self.effects:
            op = effect.run_effect()
            if not op:
                delete_effects.append(effect)

        for effect in delete_effects:
            self.effects.remove(effect)


class Phase_Out (Effect):

    def __init__(self, object, time):
        Effect.__init__(self,object, time)

    def run_effect(self):
        if "sprite" not in self.object.keys():
             return
        self.frame += 1

        self.object["sprite"].opacity = 255 - 255 * (self.frame/self.time)
        if self.frame == self.time:
            self.object["sprite"].opacity = 255
            self.frame = 0
            return False
        return True


class Phase_In (Effect):

    def __init__(self, object, time):
        Effect.__init__(self,object, time)

    def run_effect(self):
        if "sprite" not in self.object.keys():
            return
        self.frame += 1

        self.object["sprite"].opacity = 255 * (self.frame/self.time)
        if self.frame == self.time:
            self.object["sprite"].opacity = 255
            self.frame = 0
            return False
        return True


class Chain_Effect (Effect):
    effects = []

    def __init__(self, effects):
        self.effects = effects

    def run_effect(self):
        if not(self.effects[0].run_effect()):
            self.effects.remove(self.effects[0])
        return len(self.effects) > 0

class Simul_Effect(Effect):
    effects = []

    def __init__(self, effects):
        self.effects = effects

    def run_effect(self):
        for eff in self.effects:
            if not(eff.run_effect()):
                self.effects.remove(eff)
        return len(self.effects) > 0

class FadeLayerIn(Effect):
    layer = None
    def __init__(self, layer, time):
        self.layer = layer
        Effect.__init__(self,None, time)

    def run_effect(self):
        self.layer.set_opacity(255 * (self.frame/self.time))
        self.frame += 1
        if self.frame == self.time:
            self.frame = 0
            return False
        return True

class FadeLayerOut(Effect):
    layer = None
    def __init__(self, layer, time):
        self.layer = layer
        Effect.__init__(self,None, time)

    def run_effect(self):
        self.layer.set_opacity(255-255 * (self.frame/self.time))
        self.frame += 1
        if self.frame == self.time:
            self.frame = 0
            return False
        return True

