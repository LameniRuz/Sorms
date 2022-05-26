""" Entities directly controlled by players (worms, etc) """
from global_variables import *
from general_classes import Block
from collision_system import CollisionDict




# Worm class
class Worm():

    """
    Creates worm creature on the screen,
    Gives player control over it, handles behavior of the worm
    """

    def __init__(self, head_x, head_y, worm_name, global_food, global_collision_dict=CollisionDict(), **kwargs):
        """Creates worm instance. """
        # Settings
        self.color = PINK 
        self.head_color = PINK 
        self.segment_side = BLOCK_SIZE 
        self.speed = 1 
        self.start_tail_len = 2
        self.worm_name = worm_name
        self.worm_score = 0
        self.snake_mode = False

        self.alive = True 




        # Control mappings
        #Key_code mapping, maps action with the key code as a value to understand user input
        #with setting, what regulates new behavior as a key
        self.direction_keycode_map = direction_control_player_1 
        
        # Main parameters 
        self.body_segments = [] 
        self.direction = "UP" 

        # Collision dictionary
        self.global_collision_dict = global_collision_dict 

        # Food class
        self.global_food = global_food

        # Set kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

        # Add starting segments
        head = Block(x=head_x, y=head_y, side=self.segment_side, color=self.head_color)
        self.body_segments.append(head)
        self.global_collision_dict.change(head_x, head_y, self.worm_name, "Head") # Add head to the collision dict as a worm name
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
        self.global_collision_dict.change(new_seg_x, new_seg_y, self.worm_name, "Body")


    def draw(self, surface):
        # Draw body
        for sg in self.body_segments[1:]:
            sg.draw(surface)
        # Draw head on top of the body
        self.body_segments[0].draw(surface)


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
         
        # Handle Collision Detection here
        self.handle_head_collision(head_x, head_y)
        if not self.alive:
            return
        
        # Start of the movement
        head.move(head_x, head_y) # Coordinates of the head changed here

        # Add a new head position to the collision dictionary, remove old
        self.global_collision_dict.change(head_x, head_y, self.worm_name, "Head")
        self.global_collision_dict.change(old_head_coord["x"], old_head_coord["y"], 
                                          self.worm_name, "Body") # change old head position in collision dict to body

        
        # Remove old coordinates of the last element from the collision list
        last_el = self.body_segments[-1]
        self.global_collision_dict.remove(last_el.x, last_el.y) # remove old

        # Move tail to the head, next segment on the place of preceding 
        prev_seg_coord = old_head_coord
        #TODO teleport tail to the head?
        #TODO use double linked list as a worm body
        
        #Move tail to where the head needs to be
        # self.body_segments[-1].x = old_head_coord["x"]
        # self.body_segments[-1].y = old_head_coord["y"]
        
        for sg in self.body_segments[1:]:
             old_coors = {"x": sg.x, "y": sg.y}
             sg.x =  prev_seg_coord["x"]
             sg.y =  prev_seg_coord["y"]
             prev_seg_coord = old_coors
         
    def feed(self, food_x, food_y):
        self.worm_score += 1
        self.add_segment()
        self.global_food.feed_and_procreate(food_x, food_y)#NOTE this is bad design!?


    
    def handle_head_collision(self, head_x, head_y):
        #head = self.body_segments[0]
        collides_with = self.global_collision_dict.dict.get( (head_x, head_y) )

        if collides_with:
            # print(f"Collision with: {collides_with}")
            obj_owner = collides_with.get("owner")
            obj_type = collides_with.get("type")
            if obj_owner == self.worm_name:
                if obj_type != "Head":
                    # If we here we collided with own body or offspring 
                    print(f"{self.worm_name} touched its own body")
                    if self.snake_mode:
                        self.alive = False
            elif obj_type != "Food":
                # The worm has collided with other worm or obstacle and died
                print(f"{self.worm_name} is Dead!!!!")
                self.alive = False
            else:
                # we ate the food 
                self.feed(head_x, head_y)


    def update(self, surface):
        if self.alive:
            self.move()
        #self.feed(food_class_instance)
        self.draw(surface)


    def animate(self):
        pass

