import argparse
import logging
import numpy as np
from random import seed
from timeit import default_timer as timer

import pygame

import gym

import gym_racer
from gym_racer.envs.utils import getMyLogger


def parse_arguments():
    """Setup CLI interface
    """
    parser = argparse.ArgumentParser(description="Test the racer env")

    parser.add_argument("-fps", "--fps", type=int, default=1, help="frame per second")
    parser.add_argument(
        "-s", "--rand_seed", type=int, default=-1, help="random seed to use"
    )
    parser.add_argument(
        "-nf",
        "--num_frames",
        type=int,
        default=-1,
        help="how many frames to run, -1 is unlimited",
    )
    parser.add_argument(
        "-i", "--interactive", action="store_true", help="start interactive env"
    )

    # last line to parse the args
    args = parser.parse_args()
    return args


def setup_logger(logLevel="DEBUG"):
    """Setup logger that outputs to console for the module
    """
    logroot = logging.getLogger("c")
    logroot.propagate = False
    logroot.setLevel(logLevel)

    module_console_handler = logging.StreamHandler()

    #  log_format_module = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    #  log_format_module = "%(name)s - %(levelname)s: %(message)s"
    #  log_format_module = '%(levelname)s: %(message)s'
    #  log_format_module = "%(name)s: %(message)s"
    log_format_module = "%(message)s"

    formatter = logging.Formatter(log_format_module)
    module_console_handler.setFormatter(formatter)

    logroot.addHandler(module_console_handler)

    logging.addLevelName(5, "TRACE")
    # use it like this
    # logroot.log(5, 'Exceedingly verbose debug')

    # example log line
    logg = logging.getLogger(f"c.{__name__}.setup_logger")
    logg.setLevel("INFO")
    logg.debug(f"Done setting up logger")


def setup_env():
    setup_logger()

    args = parse_arguments()

    # setup seed value
    if args.rand_seed == -1:
        myseed = 1
        myseed = int(timer() * 1e9 % 2 ** 32)
    else:
        myseed = args.rand_seed
    seed(myseed)
    np.random.seed(myseed)

    # build command string to repeat this run
    # NOTE this does not work for flags, but whatever
    recap = f"python3 test_env.py"
    for a, v in args._get_kwargs():
        if a == "rand_seed":
            recap += f" --rand_seed {myseed}"
        else:
            recap += f" --{a} {v}"

    logmain = logging.getLogger(f"c.{__name__}.setup_env")
    logmain.info(recap)

    return args


def test_interactive_env(args):
    """
    """
    logg = getMyLogger(f"c.{__name__}.test_interactive_env", "INFO")
    logg.info(f"Start test_interactive_env")

    fps = args.fps
    num_frames = args.num_frames

    racer_env = gym.make("racer-v0")

    # clock for interactive play
    clock = pygame.time.Clock()

    # Main Loop
    going = True
    i = 0
    while going:
        logg.info(f"----------    ----------    New frame    ----------    ----------")

        # Handle Input Events
        # https://stackoverflow.com/a/22099654
        for event in pygame.event.get():
            logg.debug(f"Handling event {event}")
            if event.type == pygame.QUIT:
                going = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    going = False
            logg.debug(f"Done handling")

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:  # right
            action = [0, 2]
        elif keys[pygame.K_a]:  # left
            action = [0, 1]
        elif keys[pygame.K_w]:  # up
            action = [1, 0]
        elif keys[pygame.K_x]:  # down
            action = [2, 0]
        elif keys[pygame.K_q]:  # upleft
            action = [1, 2]
        elif keys[pygame.K_e]:  # upright
            action = [1, 2]
        elif keys[pygame.K_z]:  # downleft
            action = [2, 1]
        elif keys[pygame.K_c]:  # downright
            action = [2, 2]
        else:  # nop
            action = [0, 0]

        # perform the action
        obs, reward, done, info = racer_env.step(action)

        # draw the new state
        racer_env.render(reward=reward)

        # wait a bit to limit fps
        clock.tick(fps)

        if num_frames > 0:
            i += 1
            if i == num_frames:
                going = False


def test_automatic_env(args):
    """
    """
    logg = getMyLogger(f"c.{__name__}.test_automatic_env", "DEBUG")
    logg.info(f"Start test_automatic_env")

    fps = args.fps
    num_frames = args.num_frames

    racer_env = gym.make("racer-v0")

    logg.debug(f"Action Space {racer_env.action_space}")
    logg.debug(f"State Space {racer_env.observation_space}")

    going = True
    i = 0
    while going:
        logg.info(f"----------    ----------    New frame    ----------    ----------")
        start_frame = timer()

        action = racer_env.action_space.sample()
        logg.debug(f"Do the action {action}")
        mid_frame = timer()

        obs, reward, done, info = racer_env.step(action)
        racer_env.render(reward=reward)

        end_frame = timer()
        logg.debug(f"Time for sample {mid_frame-start_frame:.6f} s")
        logg.debug(f"Time for step   {end_frame-mid_frame:.6f} s")
        logg.debug(f"Time for frame  {end_frame-start_frame:.6f} s")

        logg.debug(
            f"Car state: x {info['car_pos_x']} y {info['car_pos_y']} dir {info['car_dir']}"
        )

        going = not done

        if num_frames > 0:
            i += 1
            if i == num_frames:
                going = False


if __name__ == "__main__":
    args = setup_env()
    if args.interactive:
        test_interactive_env(args)
    else:
        test_automatic_env(args)
