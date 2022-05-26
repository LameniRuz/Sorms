import pygame as pg
from pygame import draw
from pygame.locals import *
from sys import exit
from random import randrange


# import helper functions
from  helper_functions import get_keycode_mapping, get_new_pastel_rgb_color
# import globals
from global_variables import *
# import general classes
from general_classes import Block
from collision_system import CollisionDict
# import player controller classes
from player_entities import Worm
# import other player_entities 
#from world_entities import Food i deleted this file after a lot of work on it;( 
from world_entities_remake import Food 


pg.init() # Initiate pygame

# Basic set up #
screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Worms")
clock = pg.time.Clock()
score_font = pg.font.Font('./font/Pixeltype.ttf', SCORE_FTS)
alert_font = pg.font.Font('./font/Pixeltype.ttf', ALERT_FTS)


def draw_grid(surface, width, height, cell_side, color=(0,0,0)):
    columns = width // cell_side
    for col_num in range(columns + 0): # Draw vertical lines
        col_x = col_num * cell_side 
        start_pos = (col_x, 0)
        end_pos = (col_x, height)
        pg.draw.line(surface, color, start_pos, end_pos)

    rows = height // cell_side
    for row_num in range(rows + 0): # Draw horisontal lines
        row_y = row_num * cell_side 
        start_pos = (0, row_y)
        end_pos = (width, row_y)
        pg.draw.line(surface, color, start_pos, end_pos)

#TODO CREATE FONT CLASS
def display_score(players, center_x=SCREEN_WIDTH//2, center_y=0+SCORE_FTS):
    """Displays player names and scores on the screen"""
    score_txt = "Score: "
    for player in players:
        score_txt += f"{player.worm_name}: {player.worm_score}, "
    score_txt = score_txt[:-2]# Remove last ', '
    score_txt += "."
    display_font(score_txt, center_x=center_x, center_y=center_y)

def display_font(text, center_x=SCREEN_WIDTH//2, center_y=0+SCORE_FTS, font=score_font, color=GRAY, antialias=False):
    score_txt = font.render(text, antialias, color) 
    score_rect = score_txt.get_rect(center=(center_x, center_y))
    screen.blit(score_txt, score_rect)

def display_player_names(players):
    for player in players:
        x = player.body_segments[0].x + BLOCK_SIZE//2
        y = player.body_segments[0].y + BLOCK_SIZE//2
        name = player.worm_name
        display_font(name, x, y)
    


# Game class
class Game():
    """Controls game flow"""

    def __init__(self, **kwargs):
        # Settings
        self.game_speed = 150 # Higher the number = lower actual speed
        self.snake_mode = True
        self.win_countdown = 2 # to update game screen twice before the player wins, to move both player heads for the draw

        #self.TEST_STOP = False # TEST

        #background
        self.grid = False 
        self.bg_color = GOLD

        
        # Sets properties for the new game:
        #score, collision, food, empty player lists, game state
        self.set_new_game_values()
        
        # Set all kwargs as properties
        for key, value in kwargs.items():
            setattr(self, key, value)
   


    def set_new_game_values(self, active=True, pause=False):
        # Game state
        self.active = active 
        self.pause = pause

        #background
        self.draw_names = True

        # Gobal collision and food dictionaries
        self.global_collision_dict = CollisionDict() 
        self.global_food = Food(global_collision_dict=self.global_collision_dict)

        # Player control
        self.players = []
        self.active_players_num = 0
        self.active_players_idx = []


    def start_set_up(self):
        self.set_new_game_values(active=True)
        #TODO refactor this

        rnd_pastel = []
        for i in range(6):
            # Random color for the head and the body of all players
            color = tuple(get_new_pastel_rgb_color(rnd_pastel))
            rnd_pastel.append(color)

        self.player1 = Worm(BLOCK_SIZE*10, BLOCK_SIZE*10, start_tail_len=3, worm_name="Player_1", 
                            global_collision_dict=self.global_collision_dict,head_color=rnd_pastel[1], color=rnd_pastel[0],
                            global_food=self.global_food, snake_mode=self.snake_mode)

        self.player2 = Worm(SCREEN_WIDTH-BLOCK_SIZE*10, SCREEN_HEIGHT - BLOCK_SIZE*10, 
                            start_tail_len=3, worm_name="Player_2", 
                            global_collision_dict=self.global_collision_dict, color=rnd_pastel[3], head_color=rnd_pastel[2], 
                            direction_keycode_map=direction_control_player_2, direction="DOWN", 
                            global_food=self.global_food, snake_mode=self.snake_mode)

        self.player3 = Worm(BLOCK_SIZE*10, SCREEN_HEIGHT-BLOCK_SIZE*10, start_tail_len=3, worm_name="Player_3", 
                            global_collision_dict=self.global_collision_dict,head_color=rnd_pastel[4], color=rnd_pastel[5],
                            global_food=self.global_food, snake_mode=self.snake_mode,
                            direction_keycode_map=direction_control_player_3)
        self.players.append(self.player1)
        self.players.append(self.player2)
        self.players.append(self.player3)
        self.active_players_idx = [ idx for idx, _ in enumerate(self.players)]
        self.active_players_num = len(self.players)

        

        self.global_food.spawn()

    
    def place_background(self, screen):
        screen.fill(self.bg_color)
        
        if self.grid: draw_grid(screen, SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE) 
    
    def check_game_state(self):
        # Who is winning?
        #print(f"win_countdown: {win_countdown}")
        if self.active_players_num == 1:
            self.win_countdown -= 1
            if self.win_countdown == 0:
                player_idx = self.active_players_idx[0]
                worm_name = self.players[player_idx].worm_name
                display_font(f"{worm_name} has Won!", SCREEN_WIDTH//2, SCREEN_HEIGHT//2, font=alert_font)
                print(f"{worm_name} has Won!")
                self.active = False
                self.win_countdown = 2
                display_score(self.players)
        elif self.active_players_num == 0:
            display_score(self.players)
            display_font("Draw!", SCREEN_WIDTH//2, SCREEN_HEIGHT//2, font=alert_font)
            print(f"Draw!")
            self.active = False
            self.win_countdown = 2


    def game(self):
        self.start_set_up()

        # Gameloop
        while 1:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:#NOTE refactor this is messy
                        self.pause = not self.pause # toggle pause
                        if self.pause: # Do something during the pause
                            self.draw_names = True 
                        else: # start game if the pause is toggled off
                            self.active = True

                elif event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE:
                        pass

            pressed_keys = pg.key.get_pressed()
            if pressed_keys[pg.key.key_code("escape")]: # Reset the game
                self.start_set_up()

            # if pressed_keys[pg.K_SPACE]:# TODO make a better system to prevent flicks of draw_names value
                # pg.time.wait(60)  # wait to prevent flicks
                # self.draw_names = not self.draw_names
           



            if self.active:
            # if not self.TEST_STOP:
                # self.TEST_STOP = True

                # Place background surfaces or filling
                self.place_background(screen)


                # World entities
                #pass

                # Player actions 
                for player in self.players:
                    player.update(screen)

                for meta_idx, active_player_idx in enumerate(self.active_players_idx): # check alive ones
                    player = self.players[active_player_idx]
                    if not player.alive:
                        self.active_players_idx.pop(meta_idx)
                        self.active_players_num -= 1
                
                

                #Food
                self.global_food.draw(screen)

                # Check who is winning and draw the scores on the screen at the end
                self.check_game_state()
                


                # Info on top
                if self.draw_names:
                    display_player_names(self.players) 

        
                pg.display.update() # Update game screen

                if self.pause: #stop game cycle after one update on pause
                    self.active = False
                
                # Control game speed, fps
                pg.time.wait(self.game_speed) 
                clock.tick(60)





#TODO 
#DEBUG global collision dictionary 
# 1) Create event system
# 2) Handle events from the Game class 
# 3) Create food 

if __name__ == "__main__":
    game = Game(snake_mode=False)
    game.game()
