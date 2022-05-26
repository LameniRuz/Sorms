
class CollisionDict():
    """Controls and sets collision dictionary"""
    def __init__(self):
        self.dict = {}

    def change(self, x, y, owner, obj_type):
        value = { "owner": owner, "type": obj_type }
        self.set_value(x, y, value)

    def remove(self, x, y):
        self.set_value(x, y, None)

    def check_collision(self, x, y):
        collides_with = self.dict.get( (x, y) )
        if collides_with:
            return collides_with
        return False

    
    def set_value(self, x, y, value):
        self.dict[(x, y)] = value 
