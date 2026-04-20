# Gym Group Python API

A quick Python library I use to interface with the Gym Group mobile API, to retrieve information such as current gym occupancy and your gym attendance statistics.

## Simple Usage
```
from gymapi import GymGroupAPI
gym_api = GymGroupAPI('USERNAME', 'PASSWORD')

# Get gym busyness - user's home gym UUID is stored in the 'home_gym' property.
occupancy = gym_api.get_gym_occupancy(gym_api.home_gym)
```

## Scripts
```
# List all gyms (name | uuid)
./get-all-gyms.py --user USERNAME --password PASSWORD

# Get occupancy - defaults to home gym, or pass --gym for a specific UUID.
./get-occupancy.py --user USERNAME --password PASSWORD
./get-occupancy.py --user USERNAME --password PASSWORD --gym GYM_UUID
```
