import logging
import numpy as np

import pygame
from pygame.sprite import Sprite
from pygame.transform import rotate
from pygame import Surface

from gym_racer.envs.utils import getMyLogger


class RacerCar(Sprite):
    def __init__(self, pos_x, pos_y, direction=0):
        logg = logging.getLogger(f"c.{__name__}.__init__")
        logg.debug(f"Start init RacerCar")
        super().__init__()

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.precise_x = pos_x
        self.precise_y = pos_y

        self.direction = direction  # in degrees
        #  self.dir_step = 3
        self.dir_step = 15

        self.speed = 0
        self.speed_step = 1
        # viscous drag coefficient
        self.drag_coeff = 0.5

        self._create_car_image()
        self._rotate_car_image()

        # do a nop to init the correct image and rect of the sprite
        self.step("nop")

    def step(self, action):

        # pick the rotated image and place it
        self.image = self.rot_car_image[self.direction]
        self.rect = self.rot_car_rect[self.direction]
        self.rect.center = self.pos_x, self.pos_y

    def _create_car_image(self):
        """create the car sprite image and the rect

        image.set_colorkey(colorkey, RLEACCEL)
        """
        logg = logging.getLogger(f"c.{__name__}._create_car_image")
        logg.debug(f"Start _create_car_image")

        car_size = (60, 60)
        car_surf = Surface(car_size)

        black = (0, 0, 0)
        car_surf.fill(black)
        # black colors will not be blit
        car_surf.set_colorkey(black)

        wheel_color = (80, 80, 80, 0)
        wheel_len = 7
        wheel_wid = 6
        mid = wheel_wid // 2
        delta = -3

        # top left wheel
        self._draw_oval(
            car_surf, 15 + delta + mid, 10 - mid, wheel_wid, wheel_len, wheel_color
        )
        # top right wheel
        self._draw_oval(
            car_surf,
            15 + 30 - (delta + mid + wheel_len),
            10 - mid,
            wheel_wid,
            wheel_len,
            wheel_color,
        )
        # bottom left
        self._draw_oval(
            car_surf, 15 + delta + mid, 30 - mid, wheel_wid, wheel_len, wheel_color
        )
        # bottom right wheel
        self._draw_oval(
            car_surf,
            15 + 30 - (delta + mid + wheel_len),
            30 - mid,
            wheel_wid,
            wheel_len,
            wheel_color,
        )

        # body
        body_color = (255, 0, 0, 0)
        #  self._draw_oval(car_surf, 15, 10, 20, 30, body_color)
        self._draw_oval(car_surf, 19, 8, 20, 30, body_color)

        self.orig_image = car_surf

    def _draw_oval(self, surf, top, left, width, length, color):
        """draw an oval, top left is for the rectangle

        circle rect circle
        draw.rectangle(((15, 10), (45, 30)), fill="red")
        draw.ellipse(((5, 10), (25, 30)), fill="red")
        draw.ellipse(((35, 10), (55, 30)), fill="red")
        top 15 left 10 width 20 length 30

        Rect( left, top, width, height )
        """
        # make width even to simplify things
        if width % 2 != 0:
            width += 1
        mid = width // 2
        w_size = mid

        w_pos = (left, top + mid)
        pygame.draw.circle(surf, color, w_pos, w_size)
        w_pos = (left + length, top + mid)
        pygame.draw.circle(surf, color, w_pos, w_size)
        w_rect = (left, top, length, width)
        pygame.draw.rect(surf, color, w_rect)

    def _rotate_car_image(self):
        """Create rotated copies of the surface
        """
        logg = logging.getLogger(f"c.{__name__}._rotate_car_image")
        logg.debug(f"Start _rotate_car_image")
        if 360 % self.dir_step != 0:
            logg.warn(f"A dir_step that is not divisor of 360 is a bad idea")

        self.rot_car_image = {}
        self.rot_car_rect = {}
        for dire in range(0, 360, self.dir_step):
            self.rot_car_image[dire] = rotate(self.orig_image, dire)
            self.rot_car_rect[dire] = self.rot_car_image[dire].get_rect()
