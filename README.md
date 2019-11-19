# gym-racer

OpenAI gym environment of a racing car.

#### Action space

The action space is a combination of two discrete action spaces:

```
1) accelerate:  NOOP[0], UP[1], DOWN[2]
2) steer:  NOOP[0], LEFT[1], RIGHT[2]
```

#### Reward

The reward is mainly related to the direction along the street, then multiplied by the speed of the car squared.

#### Observation space

There are two types of observation possible:
* `lidar` with shape `(n)`: a lidar with n rays, each element indicates the first sensor out of the road
* `diamond` with shape `(n, n)`: a square of sensors, with a corner on the car

The observation type can be set by passing it in the call to `gym.make`, and the default parameters can be overridden by passing a `sensor_array_params` dict:

```python
sat = "lidar"       # default
#  sat = "diamond"
racer_env = gym.make(
    "racer-v0",
    sensor_array_type=sat,
    sensor_array_params=sensor_array_params,
)
```

The default parameters for the `lidar` are:

```python
sensor_array_params["ray_num"] = 7               # number of rays per side
sensor_array_params["ray_step"] = 15             # distance between sensors along a ray
sensor_array_params["ray_sensors_per_ray"] = 20  # number of sensors along a ray
sensor_array_params["ray_max_angle"] = 70        # angle to sweep left/right
```

The default parameters for the `diamond` are:

```python
sensor_array_params["viewfield_size"] = 20  # number of rows/columns in the sensor
sensor_array_params["viewfield_step"] = 10  # spacing between the dots
```

#### Render modes

There are two types of render mode available,
the `human` mode initializes `pygame` and renders what the car is doing to the screen,
while in `console` mode only the bare minimum of the `pygame` environment is loaded (to use `spritecollide`).
An environment in `console` mode cannot be rendered as `human`.

The render mode can be set by passing it in the call to `gym.make`:

```python
mode = "human"       # default
#  mode = "console"
racer_env = gym.make(
    "racer-v0",
    render_mode=mode,
)
```

#### Info
Info is a dict with some car details:

```python
keys = ["car_pos_x", "car_pos_y", "car_dir", "car_speed"]
```
