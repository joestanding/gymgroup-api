# Gym Group Python API

A quick Python library I use to interface with the Gym Group mobile API, to retrieve information such as current gym occupancy and your gym attendance statistics.

## Simple Usage
```
from gymapi import GymGroupAPI
gym_api = GymGroupAPI('USERNAME', 'PASSWORD')

# Get gym busyness - user's home gym UUID is stored in the 'home_gym' property.
occupancy = gym_api.get_gym_occupancy(gym_api.home_gym)
```
