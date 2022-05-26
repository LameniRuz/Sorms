""" Entities directly controlled by players (worms, etc) """
from global_variables import *
from general_classes import *


# Worm class
class Worm():

    """
    Creates worm creature on the screen,
    Gives player control over it, handles behavior of the worm
    """

    def __init__(self, head_x, head_y, worm_name, global_collision_dict=CollisionDict(), **kwargs):
        """Creates worm instance. """
        # Settings
        self.color = PINK 
        self.head_color = PINK 
        self.segment_side = BLOCK_SIZE 
        self.speed = 1 
        self.start_tail_len = 2
        self.worm_name = worm_name
        self.worm_score = 0

        
        # Control mappings
        #Key_code mapping, maps action with the key code as a value to understand user input
        #with setting, what regulates new behavior as a key
        self.direction_keycode_map = direction_control_player_1 
        
        # Main parameters 
        self.body_segments = [] 
        self.direction = "UP" 

        # Collision dictionary
        self.global_collision_dict = global_collision_dict 

        # Set kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

        # Add starting segments
        head = Block(x=head_x, y=head_y, side=self.segment_side, color=self.head_color)
        self.body_segments.append(head)
        self.global_collision_dict.change(head_x, head_y, self.worm_name) # Add head to the collision dict as a worm name
        for _ in range(self.start_tail_len):
            self.add_segment()

    
    def add_segment(self):
        """ Adds segment to a last existing segment 
            in the position, opposite of movement direction
        """
        last_segmt = self.body_segments[-1]
        spawn_dir = SPAWN_IN_DIR[self.direction]
        new_seg_x = last_segmt.x + (spawn_dir["x"] * self.segment_side)
        new_seg_y = last_segmt.y + (spawn_dir["y"]* self.segment_side)
        self.body_segments.append(Block(x=new_seg_x, y=new_seg_y, color=self.color))

        # Add a segment to the collision dictionary
        self.global_collision_dict.change(new_seg_x, new_seg_y, "Body")


    def draw(self, surface):
        for sg in self.body_segments:
            sg.draw(surface)


    def worm_controller(self):
        """ Handles the worm control. (player input)"""
        pressed_keys = pg.key.get_pressed()

        # Change worm direction 
        for direction, keycode in self.direction_keycode_map.items():
            if pressed_keys[keycode]:
                # Prevent instant direction change to opposite one
                current_direction = self.direction
                prevent_change_in = PREV_DIR_CHANGE[current_direction]
                if direction != prevent_change_in:
                    self.direction = direction
                    break # Very important break, prevents bug if pressed non opposite keys before movement
                    #if direction changed, stop, checking until next movement cycle 


    def move(self):
        """ Moves all segments one after another in the direction
            by the length of the segment
        """
        # Handle player input and change worm behavior if needed
        self.worm_controller()

        # Change head coordinates
        head = self.body_segments[0]
        old_head_coord = {"x": head.x, "y": head.y}
        move_dir = MOVE_IN_DIR[self.direction]
        head_x = head.x + (move_dir["x"] * self.segment_side)
        head_y = head.y + (move_dir["y"] * self.segment_side)

        # If head over the screen, teleport 
        if head_x < 0:
            head_x = SCREEN_WIDTH - self.segment_side#TEST it fixes bug i dont know why 5
        elif head_x > SCREEN_WIDTH - self.segment_side:
            head_x = 0 #works
        if head_y < 0:
            head_y = SCREEN_HEIGHT - self.segment_side
        elif head_y > SCREEN_HEIGHT - self.segment_side:
            head_y = 0 #works
         
        head.move(head_x, head_y) # Coordinates of the head changed here
        # Handle Collision Detection here
        self.detect_deadly_collision()

        # Add a new head position to the collision dictionary, remove old
        self.global_collision_dict.change(head_x, head_y, self.worm_name)
        self.global_collision_dict.change(old_head_coord["x"], old_head_coord["y"], "Body") # change old head position in collision dict to body

        
        # Remove old coordinates of the last element from the collision list
        last_el = self.body_segments[-1]
        self.global_collision_dict.change(last_el.x, last_el.y, "") # remove old

        # Move tail to the head, next segment on the place of preceding 
        prev_seg_coord = old_head_coord#TODO teleport tail to the head?
        
        #Move tail to where the head needs to be
        # self.body_segments[-1].x = old_head_coord["x"]
        # self.body_segments[-1].y = old_head_coord["y"]
        
        for sg in self.body_segments[1:]:
             old_coors = {"x": sg.x, "y": sg.y}
             sg.x =  prev_seg_coord["x"]
             sg.y =  prev_seg_coord["y"]
             prev_seg_coord = old_coors
         

    def feed(self, food_class_instance):#NOTE move this outside of the worm class 
        eaten_food_idx = self.check_collision_with_dict(food_class_instance.food_collison_dict)
        if eaten_food_idx:
            eaten_food = food_class_instance.food_blocks[eaten_food_idx]  
            food_class_instance.eat_and_procreate(eaten_food.x, eaten_food.y)

            self.worm_score += 1
            self.add_segment()

    
    
    
    def check_collision_with_dict(self, collision_dict):
        head = self.body_segments[0]
        collides_with = collision_dict.get( (head.x, head.y) )
        # print(f"collides_with: {collides_with}")
        # print(f"head x, y: {head.x}, {head.y}")

        if collides_with and collides_with != self.worm_name:
            print("Collision!!!!!")
            print(f"Collides with: {collides_with}")
            return collides_with
        return False

    def detect_deadly_collision(self, other_collision_dict=None) -> bool:
        """ Detects head collisions with the body and other unpleasant objects
        :returns: bool
        """
        # Check collision with the own body 
        own_global_collision_dict = self.check_collision_with_dict(self.global_collision_dict.dict)
        if own_global_collision_dict: return own_global_collision_dict
        
        #NOTE: we can combine the dictionaries
        # Check collision with other objects
        if other_collision_dict:
            return  self.check_collision_with_dict(other_collision_dict)
        return False


    def update(self, surface):
        self.move()
        #self.feed(food_class_instance)
        self.draw(surface)


    def animate(self):
        pass

