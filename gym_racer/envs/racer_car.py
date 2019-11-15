import logging
import numpy as np

from math import ceil

import pygame
from pygame.sprite import Sprite
from pygame.transform import rotate
from pygame import Surface

from gym_racer.envs.utils import getMyLogger


class RacerCar(Sprite):
    def __init__(self, pos_x, pos_y, direction=0):
        logg = logging.getLogger(f"c.{__name__}.__init__")
        logg.info(f"Start init RacerCar")
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

        # generate the car image and create all rotated versions
        self._create_car_image()
        self._rotate_car_image()

        # pick the correct image and place it
        self.image = self.rot_car_image[self.direction]
        self.rect = self.rot_car_rect[self.direction]
        self.rect.center = self.pos_x, self.pos_y

    def step(self, action):
        """Perform the action
        """

        # pick the rotated image and place it
        self.image = self.rot_car_image[self.direction]
        self.rect = self.rot_car_rect[self.direction]
        self.rect.center = self.pos_x, self.pos_y

    def _create_car_image(self):
        """create the car sprite image and the rect

        image.set_colorkey(colorkey, RLEACCEL)
        """
        logg = logging.getLogger(f"c.{__name__}._create_car_image")
        logg.info(f"Start _create_car_image")

        # wheel dimensions
        w_color = (80, 80, 80)
        w_len = 7  # horizontal length of the wheel
        w_radius = 3
        w_wid = w_radius * 2
        delta = -3  # space from car to wheel

        # car dimensions
        car_wid = 20
        car_len = 30
        # place the car so that it touches the border of the surf
        car_top = w_radius
        car_left = ceil(car_wid / 2)

        # create a surf just big enough for the car
        car_surf_size = (car_len + car_wid, car_wid + w_wid)
        car_surf = Surface(car_surf_size)
        # convert the surface for fastest blitting
        # same pixel format as the display Surface
        car_surf = car_surf.convert()

        black = (0, 0, 0)
        car_surf.fill(black)
        # black colors will not be blit
        #  car_surf.set_colorkey(black)
        # RLEACCEL should make blitting faster
        car_surf.set_colorkey(black, pygame.RLEACCEL)
        # show the surface area to debug
        #  car_surf.fill((0, 0, 255))

        # top left wheel
        w_top = car_top - w_radius
        w_left = car_left + delta + w_radius
        self._draw_oval(car_surf, w_top, w_left, w_wid, w_len, w_color)

        # top right wheel
        w_top = car_top - w_radius
        w_left = car_left + car_len - (delta + w_radius + w_len)
        self._draw_oval(car_surf, w_top, w_left, w_wid, w_len, w_color)

        # bottom left wheel
        w_top = car_top + car_wid - w_radius
        w_left = car_left + delta + w_radius
        self._draw_oval(car_surf, w_top, w_left, w_wid, w_len, w_color)

        # bottom right wheel
        w_top = car_top + car_wid - w_radius
        w_left = car_left + car_len - (delta + w_radius + w_len)
        self._draw_oval(car_surf, w_top, w_left, w_wid, w_len, w_color)

        # body
        body_color = (255, 0, 0)
        self._draw_oval(car_surf, car_top, car_left, car_wid, car_len, body_color)

        # windshield
        wind_wid1 = 4
        wind_wid2 = 7
        # vertical mid point
        wind_mid = car_top + car_wid // 2
        # horizontal points 52 46 36 36 46
        wind_hpos = car_len - 2
        d1 = 10
        d2 = 16
        wind_points = [
            (wind_hpos + d2, wind_mid - 1),
            (wind_hpos + d1, wind_mid - wind_wid2),
            (wind_hpos, wind_mid - wind_wid1),
            (wind_hpos, wind_mid + wind_wid1 - 1),
            (wind_hpos + d1, wind_mid + wind_wid2 - 1),
            (wind_hpos + d2, wind_mid),
        ]
        wind_color = (0, 255, 255)
        pygame.draw.polygon(car_surf, wind_color, wind_points)

        self.orig_image = car_surf

    def _draw_oval(self, surf, top, left, width, length, color):
        """draw an oval on Surface surf

        horizontal circle-rect-circle 
        top left is for the rectangle
        width is the height, length is the width lol
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
        # constructor Rect( left, top, width, height )
        w_rect = (left, top, length, width)
        pygame.draw.rect(surf, color, w_rect)

    def _rotate_car_image(self):
        """Create rotated copies of the surface
        """
        logg = logging.getLogger(f"c.{__name__}._rotate_car_image")
        logg.info(f"Start _rotate_car_image")
        if 360 % self.dir_step != 0:
            logg.warn(f"A dir_step that is not divisor of 360 is a bad idea")

        self.rot_car_image = {}
        self.rot_car_rect = {}
        for dire in range(0, 360, self.dir_step):
            self.rot_car_image[dire] = rotate(self.orig_image, dire)
            self.rot_car_rect[dire] = self.rot_car_image[dire].get_rect()
