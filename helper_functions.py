""" Helper functions """
import pygame as pg
from random import randint, random, uniform
from colorsys import hsv_to_rgb

from pygame.event import event_name

def get_keycode_mapping(control_mapping):
    """ Translates control mapping dictionary to key_code mapping dictionary"""
    keycode_mapping = {}
    for setting, keyname in control_mapping.items():
        keycode_mapping[setting] = pg.key.key_code(keyname)
    return keycode_mapping


def get_random_pastel_hsl_color():
    hue = uniform(0, 360) 
    saturation = 25 + (70 * uniform(0, 1.0)) # from 25 to 95
    lightness = 85 + (10 * uniform(0, 1.0)) # from 85 to 95
    return [hue, saturation, lightness]


def gen_random_color_cmy(pseudo_pastel_factor = 0.8):
    random_colors = [uniform(0,1.0) for _ in range(3)]
    return [(old_color + pseudo_pastel_factor) / (1.0 + pseudo_pastel_factor) for old_color in random_colors]

def get_sum_channel_color_distance(color_1, color_2):
    return sum([abs(channel[0] - channel[1]) for channel in zip(color_1, color_2)])

def get_new_cmy_color(existing_colors, pseudo_pastel_factor=0.5):
    pass

def get_new_pastel_rgb_color(existing_rgb_colors=[], distinctness_dist=140, attempts=150):
    """Attempts to generate a new random pastel color, different from the existing,
    based on the distance between an existing and a new color in the span of given attempts"""
    last_furthest_rnd_pastel = {"min_distance": 0, "color": None} 
    
    for _ in range(attempts):
        
        # Get random pastel color
        rnd_pastel = get_random_pastel_hsl_color()
        h, s, v = rnd_pastel
        rnd_pastel = [round(color * 255) for color in hsv_to_rgb(h/360, s/100, v/100)] # turn hsv to non normalised rgb
        if not existing_rgb_colors:
            return rnd_pastel
        
        # Check if its to close to other existing color
        closest_to_existing_dist = min([get_sum_channel_color_distance(rnd_pastel, exist_clr) 
                                    for exist_clr in existing_rgb_colors])
        if closest_to_existing_dist >= distinctness_dist:# If color far enough from the others, return it
            return rnd_pastel
        # Save last best (furthest result)
        if last_furthest_rnd_pastel["min_distance"] < closest_to_existing_dist:
            last_furthest_rnd_pastel["min_distance"] = closest_to_existing_dist
            last_furthest_rnd_pastel["color"] = closest_to_existing_dist
    # returns furthest generated color yet in the worst case scenario
    return last_furthest_rnd_pastel["color"]

if __name__ == "__main__":

    colors_num = 10
    random_colors = []
    tint_factor = 0.4
    pseudo_pastel_factor= 0.5
    for i in range(colors_num):
        
        #cmy_color = gen_random_color_cmy(pseudo_pastel_factor)
        #pg_color.cmy = tuple(cmy_color)

        # hsv_color = get_random_pastel_hsl_color()
        # hsv_color += [100]
        # pg_color = pg.Color(0,0,0)
        # pg_color.hsva = tuple(hsv_color)
        pg_color = tuple(get_new_pastel_rgb_color(random_colors))
        random_colors.append(pg_color)
    print(random_colors)

    screen = pg.display.set_mode((300,300))
    clock = pg.time.Clock()

    color_idx = 0
    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
        print(color_idx) 
        screen.fill(tuple(random_colors[color_idx]))

        color_idx += 1
        if color_idx > colors_num-1:
            color_idx = 0
        
        pg.display.update()
        clock.tick(1)





