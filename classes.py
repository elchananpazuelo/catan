import settings

class Block:
    def __init__(self, block_type, level=1.0):
        self.block_type = block_type
        self.sound_path = settings.SOUNDS[block_type]

class Player:
    def __init__(self, XP=1.0):
        self.resources = {
            "wool": 0,
            "wood": 0,
            "brick": 0,
            "iron": 0,
            "wheat": 0
        }
        
        self.XP = XP
    
    def add_resource(self, resource_type, amount=1):
        if resource_type in self.resources:
            self.resources[resource_type] += amount

    def can_afford(self, cost_dict,building):
        if self.XP < cost_dict[building]:
            return False
        self.XP -= cost_dict["building"]
        return True

    def convert_to_xp(self,xp_map,resource_type,amount):
        if self.resources[resource_type] < amount:
            return 
        else:
            self.XP += xp_map[resource_type] * amount
            self.XP = round(self.XP, 2)
            self.resources[resource_type] -= amount
    
        