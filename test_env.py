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
    recap = f"python3 lab03_main.py"
    for a, v in args._get_kwargs():
        if a == "rand_seed":
            recap += f" --rand_seed {myseed}"
        else:
            recap += f" --{a} {v}"

    logmain = logging.getLogger(f"c.{__name__}.setup_env")
    logmain.info(recap)

    return args


def run_test_env(args):
    """
    """
    logg = getMyLogger(f"c.{__name__}.run_test_env", "INFO")
    logg.info(f"Start run_test_env")

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
        if keys[pygame.K_d]:
            racer_env.step("right")
        elif keys[pygame.K_a]:
            racer_env.step("left")
        elif keys[pygame.K_w]:
            racer_env.step("up")
        elif keys[pygame.K_x]:
            racer_env.step("down")
        elif keys[pygame.K_q]:
            racer_env.step("upleft")
        elif keys[pygame.K_e]:
            racer_env.step("upright")
        elif keys[pygame.K_z]:
            racer_env.step("downleft")
        elif keys[pygame.K_c]:
            racer_env.step("downright")
        else:
            racer_env.step("nop")

        clock.tick(fps)

        if num_frames > 0:
            i += 1
            if i == num_frames:
                going = False


if __name__ == "__main__":
    args = setup_env()
    run_test_env(args)
