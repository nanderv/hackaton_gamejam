__author__ = 'nander'

class GameState():
     INSTANCE = None

     def __init__(self):
        if self.INSTANCE is not None:
            raise ValueError("An instantiation already exists!")
        # do your init stuff

     @classmethod
     def get_instance(cls):
        if cls.INSTANCE is None:
             cls.INSTANCE = GameState()
        return cls.INSTANCE
