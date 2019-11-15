import logging
import numpy as np

from pygame import Surface
from pygame.sprite import Group
from pygame.sprite import Sprite
from pygame.transform import rotate
from pygame import draw

from gym_racer.envs.utils import getMyLogger


class RacerMap(Group):
    """Map for a racer, as collection of Segment

    Should be easy to do collision detection
    """

    def __init__(self, field_wid, field_hei):
        logg = getMyLogger(f"c.{__name__}.__init__", "INFO")
        logg.info(f"Start init RacerMap")
        super().__init__()

        self.field_wid = field_wid
        self.field_hei = field_hei

        self._create_road_segment()

        # direction, centerx, centery
        self.seg_info = [
            [0, 200, 100],
            [270, 450, 200],
            [0, 550, 450],
            [270, 800, 550],
            [180, 700, 800],
            [180, 350, 800],
            [90, 100, 700],
            [90, 100, 350],
        ]
        self.segments = {}
        self.num_segments = len(self.seg_info)

        # create the various segments, with unique id_
        for id_ in range(self.num_segments):
            direction, cx, cy = self.seg_info[id_]
            self.segments[id_] = Segment(self.segment_orig, direction, cx, cy, id_)
            # register the segment as a Sprite in the Group
            self.add(self.segments[id_])

        self._precompute_map()

    def _create_road_segment(self):
        """Create the bmp for a road segment
        """
        logg = getMyLogger(f"c.{__name__}._create_road_segment")

        self.segment_wid = 350
        self.segment_hei = 150
        line_wid = 2
        mid_hei = self.segment_hei // 2

        seg_surf = Surface((self.segment_wid, self.segment_hei))
        seg_surf = seg_surf.convert()
        segment_grey = (128, 128, 128)
        seg_surf.fill(segment_grey)

        # Rect(left, top, width, height) -> Rect
        line_white = (255, 255, 255)
        line_rect = 0, mid_hei - line_wid, self.segment_wid, line_wid
        draw.rect(seg_surf, line_white, line_rect)
        line_rect = self.segment_wid - line_wid, 0, line_wid, self.segment_hei
        draw.rect(seg_surf, line_white, line_rect)

        self.segment_orig = seg_surf

    def _precompute_map(self):
        """turn the map into a np array for fast sensor collision lookup

        MAYBE add a map with s_id in it and do the car/road collision with that
        """
        logg = getMyLogger(f"c.{__name__}._precompute_map", "INFO")
        logg.debug(f"Start _precompute_map")

        self.raw_map = np.zeros((self.field_wid, self.field_hei), dtype=np.uint8)
        for i in self.segments:
            rect = self.segments[i].rect
            logg.debug(f"rect {rect}")
            logg.debug(
                f"left {rect.left} right {rect.right} top {rect.top} bottom {rect.bottom}"
            )
            self.raw_map[rect.left : rect.right, rect.top : rect.bottom] = 1


class Segment(Sprite):
    """A single segment of road
    """

    def __init__(self, segment_orig, direction, cx, cy, s_id):
        logg = getMyLogger(f"c.{__name__}.__init__", "INFO")
        logg.debug(f"Start init")
        super().__init__()

        self.direction = direction
        self.cx = cx
        self.cy = cy
        self.s_id = s_id

        self.image = rotate(segment_orig, self.direction)
        self.rect = self.image.get_rect(center=(self.cx, self.cy))
