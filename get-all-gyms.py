#!/usr/bin/env python3

import argparse
from gymapi import GymGroupAPI

parser = argparse.ArgumentParser()
parser.add_argument('--user', required=True)
parser.add_argument('--password', required=True)
args = parser.parse_args()

gym_api = GymGroupAPI(args.user, args.password)

gyms = gym_api.get_all_gyms()

for gym in gyms:
    name = gym.get('name')
    uuid = gym.get('uuid')
    print(f"{name} | {uuid}")
