from abc import ABC, abstractmethod
import numpy as np
import time
import random

# Return the colour some fraction of the way betwen two rgb colours
def inbetween_color(color1, color2, fraction):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    r = int(r1 + (r2 - r1) * fraction)
    g = int(g1 + (g2 - g1) * fraction)
    b = int(b1 + (b2 - b1) * fraction)
    return (r, g, b)

# Return the colour some fraction of the way through a whole sequence of colours
def get_color_in_sequence(color_list, fraction):
    list_index = np.floor(fraction * len(color_list))
    color1 = color_list[int(list_index)]
    color2 = color_list[int(list_index + 1) % len(color_list)]
    list_fraction = fraction * len(color_list) - list_index
    return inbetween_color(color1, color2, list_fraction)


class Effect(ABC):
    def __init__(self, leds, positions, fps=60):
        self.leds = leds
        self.positions = positions
        self.fps = fps

    def run(self):
        self.leds.set_all_off()
        self.setup()

        try:
            while True:
                self.draw()
                self.leds.show()
                time.sleep(1 / self.fps)

        except:
            self.leds.set_all_off()
            raise

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def draw(self):
        pass

class WaveEffect2D(Effect):
    def __init__(self, leds, positions, color_list, duration=1, fps=60, direction='x'):
        super().__init__(leds, positions, fps)
        
        self.duration = duration
        self.color_list = color_list
        self.direction = direction

    
    def setup(self):
        '''Run at the start of the effect'''
        self.min_x = min(self.positions, key=lambda x: x[0])[0]
        self.max_x = max(self.positions, key=lambda x: x[0])[0]
        self.min_y = min(self.positions, key=lambda x: x[1])[1]
        self.max_y = max(self.positions, key=lambda x: x[1])[1]

        
        self.center_x = (self.min_x + self.max_x) / 2
        self.center_y = (self.min_y + self.max_y) / 2

        self.x_rel = (self.positions[:, 0] - self.min_x) / (self.max_x - self.min_x)
        self.y_rel = (self.positions[:, 1] - self.min_y) / (self.max_y - self.min_y)

        self.effect_progress = 0 # goes from 0 to 1
        
        # self.directions = ['x', 'y']
        # self.direction = random.choice(self.directions)

    def draw(self):
        '''Run every frame'''

        if self.effect_progress >= 1:
            self.effect_progress = 0
            # self.direction = random.choice(self.directions)

        # Set each LED to the right colour
        for i in range(len(self.leds)):

            # Get the LED position
            x, y = self.positions[i]

            if self.direction == 'x':
                # ----- left/right wave -----
                # Relative x position
                p = self.x_rel[i]

            if self.direction == 'y':
                # ----- front/back wave -----
                # Relative y position
                p = self.y_rel[i]
            

            # Skip if p is nan
            if np.isnan(p):
                continue

            # p is the increase in progress for the current pixel
            # Calculate the color
            color = get_color_in_sequence(
                self.color_list, 
                (self.effect_progress + p) % 1
            )

            # Set the colour
            self.leds[i] = color
        
        # Increment the effect progress
        self.effect_progress += 1 / (self.duration * self.fps)


class TextScroll2D(Effect):
    def __init__(self, leds, positions, color_list, duration=1, fps=60):
        super().__init__(leds, positions, color_list, duration, fps)
        
        self.direction = direction

    
    def setup(self):
        '''Run at the start of the effect'''
        self.min_x = min(self.positions, key=lambda x: x[0])[0]
        self.max_x = max(self.positions, key=lambda x: x[0])[0]
        self.min_y = min(self.positions, key=lambda x: x[1])[1]
        self.max_y = max(self.positions, key=lambda x: x[1])[1]

        self.x_rel = (self.positions[:, 0] - self.min_x) / (self.max_x - self.min_x)
        self.y_rel = (self.positions[:, 1] - self.min_y) / (self.max_y - self.min_y)

        self.effect_progress = 0 # goes from 0 to 1
        
        # self.directions = ['x', 'y']
        # self.direction = random.choice(self.directions)

    def draw(self):
        '''Run every frame'''

        if self.effect_progress >= 1:
            self.effect_progress = 0
            # self.direction = random.choice(self.directions)

        # Set each LED to the right colour
        for i in range(len(self.leds)):

            # Get the LED position
            x, y = self.positions[i]

            if self.direction == 'x':
                # ----- left/right wave -----
                # Relative x position
                p = self.x_rel[i]

            if self.direction == 'y':
                # ----- front/back wave -----
                # Relative y position
                p = self.y_rel[i]
            

            # Skip if p is nan
            if np.isnan(p):
                continue

            # p is the increase in progress for the current pixel
            # Calculate the color
            color = get_color_in_sequence(
                self.color_list, 
                (self.effect_progress + p) % 1
            )

            # Set the colour
            self.leds[i] = color
        
        # Increment the effect progress
        self.effect_progress += 1 / (self.duration * self.fps)
