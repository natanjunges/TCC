#!/usr/bin/env python3

from RobotAgent import RobotAgent
from HumanAgent import HumanAgent
from State import State
import random
import sys
import json

if __name__ == "__main__":
    path_prefix = "."

    with open(path_prefix + "/objects.json", "r") as file:
        objects = json.load(file)

    id = 1
    #seed = 0
    seed = random.randrange(sys.maxsize)
    #interaction = State.FirstInteraction
    interaction = State.SecondInteraction
    noise = 0.1
    robot = RobotAgent(id, path_prefix, seed, noise, interaction, len(objects))
    human = HumanAgent(id, path_prefix, seed, noise, interaction, objects)
    human.connect(robot)
    robot.start()
    human.start()
    robot.join()
    human.join()
