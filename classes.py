import settings

class Block:
    def __init__(self, block_type, level=1.0):
        self.block_type = block_type
        self.sound_path = settings.SOUNDS[block_type]

class Player:
    def __init__(self, XP=1.0):
        self.XP = XP


