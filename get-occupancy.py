#!/usr/bin/env python3

import argparse
from gymapi import GymGroupAPI

parser = argparse.ArgumentParser()
parser.add_argument('--user', required=True)
parser.add_argument('--password', required=True)
parser.add_argument('--gym')
args = parser.parse_args()

gym_api = GymGroupAPI(args.user, args.password)

gym_uuid = args.gym if args.gym else gym_api.home_gym

gym = gym_api.get_gym(gym_uuid)
occupancy = gym_api.get_gym_occupancy(gym_uuid)

print(f"Occupancy for '{gym['name']}': {occupancy}")
