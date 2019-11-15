import gym
import pygame

from pygame.sprite import spritecollide

from gym_racer.envs.utils import getMyLogger
from gym_racer.envs.racer_car import RacerCar
from gym_racer.envs.racer_map import RacerMap


class RacerEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self, field_wid, field_hei):
        """
        """
        logg = getMyLogger(f"c.{__class__.__name__}.__init__")
        logg.info(f"Start init RacerEnv")

        # racing field dimensions
        self.field_wid = field_wid
        self.field_hei = field_hei
        self.field_size = (self.field_wid, self.field_hei)

        # sidebar info dimensions
        self.sidebar_wid = 300
        self.sidebar_hei = self.field_hei
        self.sidebar_size = (self.sidebar_wid, self.sidebar_hei)

        # total dimensions
        self.total_wid = self.sidebar_wid + self.field_wid
        self.total_hei = self.field_hei
        self.total_size = (self.total_wid, self.total_hei)

        # start pygame
        pygame.init()
        self.screen = pygame.display.set_mode(self.total_size)
        pygame.display.set_caption("Racer")

        # create the background that will be redrawn each iteration
        self.background = pygame.Surface(self.total_size)
        self.background = self.background.convert()

        # Create the playing field
        self.field = pygame.Surface(self.field_size)
        self.field = self.field.convert()
        self.field.fill((0, 0, 0))

        # where the info will be
        self._setup_sidebar()

        # setup the agent
        self.racer_car = RacerCar(100, 100)

        # add the car to the list of sprites to render
        self.allsprites = pygame.sprite.RenderPlain((self.racer_car))

        # setup the road
        self.racer_map = RacerMap(self.field_wid, self.field_hei)
        # draw map on the field, it is static, so there is no need to redraw it every time
        self.racer_map.draw(self.field)

        # draw the field (with the map on it) on the background
        self.background.blit(self.field, (0, 0))

        # Define action and observation space TODO

    def step(self, action):
        """
        # Execute one time step within the environment
        """
        logg = getMyLogger(f"c.{__class__.__name__}.step")
        logg.info(f"Start env step, action: '{action}'")

        # update the car
        self.racer_car.step(action)

        # compute the reward for this action
        reward, done = self._compute_reward()

        # draw the new state
        self.render()

    def reset(self):
        """
        # Reset the state of the environment to an initial state
        """

    def render(self, mode="human", close=False):
        """
        # Render the environment to the screen
        """
        # TODO only if render is active
        self._update_display()

    def _compute_reward(self):
        """compute the reward for moving on the map
        """
        logg = getMyLogger(f"c.{__class__.__name__}._compute_reward")
        logg.debug(f"Start _compute_reward")

        # compute collision car/road
        hits = spritecollide(self.racer_car, self.racer_map, dokill=False)
        #  logg.debug(f"hitting {hits}")
        hit_directions = []
        hit_sid = []
        for segment in hits:
            logg.debug(f"hit segment with id {segment.s_id}")
            hit_directions.append(self.racer_map.seg_info[segment.s_id][0])
            hit_sid.append(segment.s_id)

        # out of the map
        if len(hit_directions) == 0:
            return 0, True

        # too many hits, your road is weird, cap them at 2 segments
        elif len(hit_directions) > 2:
            logg.warn(f"Too many segments hit")
            hit_directions = hit_directions[:2]
            hit_sid = hit_sid[:2]

        # now hit_directions is either 1 or 2 elements long
        if len(hit_directions) == 1:
            mean_direction = hit_directions[0]
        else:
            # 135   90  45    140   95  50    130   85  40
            # 180       0     185       5     175       -5
            # 225   270 315   230   275 320   220   265 310
            # 270, 0 have mean 315 = (270+0+360)/2
            # 270, 180 have mean 225 = (270+180)/2
            # 0, 90 have mean 45 = (0+90)/2
            if abs(hit_directions[0] - hit_directions[1]) > 180:
                mean_direction = (sum(hit_directions) + 360) / 2
                if mean_direction >= 360:
                    mean_direction -= 360
            else:
                mean_direction = sum(hit_directions) / 2

        error = self.racer_car.direction - mean_direction
        if error < 0:
            error += 360
        if error > 180:
            error = 360 - error
        logg.debug(f"direction {self.racer_car.direction} has error of {error:.4f}")

        reward = 90 - error
        # MAYBE a sigmoid-like shape
        return reward, False

    def _setup_sidebar(self):
        """
        """
        logg = getMyLogger(f"c.{__class__.__name__}._setup_sidebar")
        logg.info(f"Start _setup_sidebar")

        # setup fonts to display info
        self._setup_font()

        # create the sidebar surface
        self.sidebar_surf = pygame.Surface(self.sidebar_size)
        self.sidebar_surf = self.sidebar_surf.convert()
        self.sidebar_surf.fill((80, 80, 80))

        # add titles
        speed_text_hei = 200
        text_speed = self.main_font.render("Speed:", 1, (255, 255, 255))
        textpos_speed = text_speed.get_rect(
            center=(self.sidebar_wid // 2, speed_text_hei)
        )
        self.sidebar_surf.blit(text_speed, textpos_speed)

        direction_text_hei = 300
        text_direction = self.main_font.render("Direction:", 1, (255, 255, 255))
        textpos_direction = text_direction.get_rect(
            center=(self.sidebar_wid // 2, direction_text_hei)
        )
        self.sidebar_surf.blit(text_direction, textpos_direction)

        # setup positions for dynamic info: blit the text on a secondary
        # surface, then blit that on the screen in the specified position
        val_delta = 50
        self.speed_val_wid = self.sidebar_wid // 2
        self.speed_val_hei = speed_text_hei + val_delta
        self.direction_val_wid = self.sidebar_wid // 2
        self.direction_val_hei = direction_text_hei + val_delta

        # draw the sidebar on the background
        self.background.blit(self.sidebar_surf, (self.field_wid, 0))

    def _setup_font(self):
        """
        """
        if not pygame.font:
            logg.critical("You need fonts to put text on the screen")
        # create a new Font object (from a file if you want)
        self.main_font = pygame.font.Font(None, 36)

    def _update_display(self):
        """draw everything
        """
        logg = getMyLogger(f"c.{__class__.__name__}._update_display")
        logg.debug(f"Start _update_display")

        # Draw Everything again, every frame
        # the background already has the road and sidebar template drawn
        self.screen.blit(self.background, (0, 0))

        # draw all moving sprites (the car) on the screen
        self.allsprites.draw(self.screen)
        # if you draw on the field you can easily leave a track
        #  allsprites.draw(field)

        # update the display
        pygame.display.flip()
