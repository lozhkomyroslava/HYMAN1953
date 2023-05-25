#! /usr/bin/env python

import numpy as np
import math
from expyriment import design, control, stimuli
import time
import pygame
import random


min_time = 1000
max_time = 2000
response_delay = 4000
exp = design.Experiment(name="multitask")
control.initialize(exp)

training_trails = 4
block = 3
trails_in_block = 4
total_trails = block*trails_in_block
result = 'rection_time_1.csv'

exp = design.Experiment(name="multitask")
control.initialize(exp)

# screen and canvas setting
white=(255,255,255)
blankscreen = stimuli.BlankScreen(colour=white)
frame_size=(400,300)
black = (0,0,0)
font_size = 32
shape_text = "SHAPE"
filling_text = "FILLING"
screen_size = exp.screen.size


# make canvas
frame1 = stimuli.Rectangle(
frame_size, colour=black,
position=(0, 0 - frame_size[1]/2),
line_width=2
)

frame2 = stimuli.Rectangle(
frame_size, colour=black,
position=(0, 0 + frame_size[1]/2),
line_width=2
)
shape = stimuli.TextLine(
shape_text,
position=(0, 0 - (frame_size[1]) - 2*font_size),
text_size=font_size
)

filling = stimuli.TextLine(
filling_text,
position=(0, 0 + (frame_size[1]) + 2*font_size),
text_size=font_size
)

# make stimuli matrix
s_name = ['d_2_dots', 'd_3_dots', 's_2_dots', 's_3_dots']
s_index = np.repeat([0,1,2,3],training_trails/4)
index_meaning = {0: 'diamond2', 1: 'diamond3', 2:'square2' , 3: 'square3'}
random.shuffle(s_index)
s_position = [(0 , - frame_size[1]/2), (0 , frame_size[1]/2)]
position_index = np.repeat([0,1],training_trails/2)
position_meaning = {0:'shape',1:'filling'}
random.shuffle(position_index)
keymeaning = {102:'f', 106:'j'}

instructions = stimuli.TextScreen("Instructions",
    f"""Welcome to the multi-task experiment.

    There will be a diamond or a square appearing on the screen, with two or three dots in it.

    If the stimuli appears on the upper half of the screen, please indicate the shape you see,

    press F for diamond and press J for square.

    Otherwise, if the stimuli appears on the bottom half of the screen, please indicate the number of dots you see,

    press F for 2 dots and press J for 3 dots.

    Your task is to press the SPACEBAR as quickly and correctly as possible when you see it.

    There will be {total_trails} trials in total.

    Press the spacebar to start.""")


control.start(skip_ready_screen=True)
instructions.present()
exp.keyboard.wait()

start_time = time.time()
end_time = time.time()
reaction_time = end_time - start_time

# first block
for i in range(training_trails):
    try:
        frame1.plot(blankscreen)
        frame2.plot(blankscreen)
        shape.plot(blankscreen)
        filling.plot(blankscreen)
        blankscreen.present()

        waiting_time = random.randint(min_time, max_time)
        exp.clock.wait(waiting_time)

        image = stimuli.Picture(s_name[s_index[i]] + '.png')
        image.anchor = (0.5, 0.5)  # set the anchor to the center of the image
        image.position = s_position[position_index[i]] 
        image.plot(blankscreen)
        blankscreen.present()

        
        key, rt = exp.keyboard.wait(duration=response_delay)
        key = keymeaning[key]
        exp.data.add([i, waiting_time, key, rt, position_meaning[position_index[i]], index_meaning[s_index[i]]])
        blankscreen.clear_surface()
        blankscreen.present()
        exp.clock.wait(1000)

        end_time = time.time()

    except Exception as e:
        print(f"Error loading image: {e}")

def measure_reaction_time(max_response_delay=2000):
    button_pressed = False
    escape = False
    response_delay_elapsed = False
    reaction_time = 0
    pygame.event.clear()  # anticipations will be ignored
    t0 = pygame.time.get_ticks()

    while not button_pressed and not escape and not response_delay_elapsed:
        for ev in pygame.event.get():
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                escape = True
                break
            if ev.type == pygame.QUIT:
                escape = True
                break
            if ev.type == pygame.MOUSEBUTTONDOWN or ev.type == pygame.KEYDOWN:
                reaction_time = pygame.time.get_ticks() - t0
                button_pressed = True

        if pygame.time.get_ticks() - t0 > MAX_RESPONSE_DELAY:
            response_delay_elapsed = True

    if escape:
        return None
    else:
        return reaction_time

def save_data(waiting_times, reaction_times, filename=result):
    with open(filename, 'wt') as f:
        f.write('Wait,RT\n')
        for wt, rt in zip(waiting_times, reaction_times):
            f.write(f"{wt},{rt}\n")

control.end()

# # # output response times
# for i_trial in range(total_trails):
#     blankscreen.present()
#     waiting_time = random.randint(min_time, max_time)
#     exp.clock.wait(waiting_time)
#     target.present()
#     key, rt = exp.keyboard.wait(duration=response_delay)
#     exp.data.add([training_trails, waiting_time, key, rt])
