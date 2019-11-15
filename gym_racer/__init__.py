from gym.envs.registration import register

# define the name to call the env
# gym.make("racer-v0")
register(id="racer-v0", entry_point="gym_racer.envs:RacerEnv")
