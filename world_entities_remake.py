from general_classes import Block
from global_variables import *
#from collision_system import CollisionDict
from random import randrange 
from player_entities import Worm

class Food():

    def __init__(self, global_collision_dict, **kwargs):
        self.food_dict = {}
        self.color = GREEN
        self.global_collision_dict = global_collision_dict
        self.min_spawn = 1
        self.max_spawn = 2

        for key, value in kwargs.items():
            setattr(self, key, value)
        
    
    def destroy(self, food_x, food_y):
        """Removes food block form collision_system and food_dict"""
        self.global_collision_dict.remove(food_x, food_y)
        return self.food_dict.pop( (food_x, food_y) )

    def create(self, food_x, food_y):
        """Adds food block to collision_system and food_dict"""
        self.food_dict[ (food_x, food_y) ] = Block(x=food_x, y=food_y, color=self.color)
        self.global_collision_dict.set_value(food_x, food_y, {"owner": "World", "type": "Food"})
    
    def get_random_coord(self):
        food_x = randrange(0, SCREEN_WIDTH - BLOCK_SIZE+1, BLOCK_SIZE)
        food_y = randrange(0, SCREEN_HEIGHT - BLOCK_SIZE+1, BLOCK_SIZE)
        return food_x, food_y

    def spawn_random_food(self):
        food_x, food_y = self.get_random_coord()
        while self.global_collision_dict.check_collision(food_x, food_y): # Not efficient, if food exist, create new random coord
            food_x, food_y = self.get_random_coord()
        self.create(food_x, food_y)

    def spawn(self):
        create_qty = randrange(self.min_spawn, self.max_spawn+1) # How many new food block create?
        for _ in range(create_qty):
            self.spawn_random_food()


    def feed_and_procreate(self, food_x, food_y):
        self.destroy(food_x, food_y)
        self.spawn()


    def draw(self, surface):
        for _, food in self.food_dict.items():
            food.draw(surface)

class EnemyWorm(Worm):
    def __init__(self, head_x, head_y, worm_name, global_food, global_collision_dict, **kwargs):
        super().__init__(head_x, head_y, worm_name, global_food, global_collision_dict, **kwargs)
    

    def go_to_random_food(self):
        pass
   
    
    def change_direction(self, new_direction):
        """Changes worm direction if posiible,returns True if direction is changed
        if direction is changes to the opposite one, returns False, direction remains
        """
        current_direction = self.direction
        prevent_change_in = PREV_DIR_CHANGE[current_direction]
        if new_direction != prevent_change_in:
            self.direction = new_direction 
            return True
        return False


    def go_to_coord_x_or_y(self, target_crd, head_crd, head_grtr_dir, head_sml_dir):
        """move head in head_grtr_dir if head coord greater than target
            or  in head_sml_dir otherwise, depending on the target_x/or y and the head_x/or y
           if change is impossible or if 'head_x/or y == target_x/or y', return false 
           
           Directions: LEFT, RIGHT, UP, DOWN
        """#NOTE in development
        if head_crd > target_crd:
            #Go left
            return self.change_direction("LEFT")
        if head_crd < target_crd: 
            #Go right 
            return self.change_direction("RIGHT")
        return False


    def go_to_coords(self, target_x, target_y):
        head = self.body_segments[0]
        head_x = head.x
        head_y = head.y

        dist_hx_x = abs( abs(target_x) - abs(head_x) )
        dist_hy_y = abs( abs(target_y) - abs(head_y) )
        
        x_dir_change = False 
        y_dir_change = False 
        if dist_hx_x > dist_hy_y: # Move to the pair of directions with thi largest distance 
            x_dir_change = self.go_to_coord_x_or_y(target_x, head_x, "LEFT","RIGHT") 
            if not x_dir_change:
                y_dir_change = self.go_to_coord_x_or_y(target_y, head_y, "UP","DOWN") 

        else:
            y_dir_change = self.go_to_coord_x_or_y(target_y, head_y, "UP","DOWN") 
            if not y_dir_change:
                x_dir_change = self.go_to_coord_x_or_y(target_x, head_x, "LEFT","RIGHT") 


    def worm_controller(self):#TODO remove this method later?!?
        return False 






