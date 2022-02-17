#!/usr/bin/env python3

from RobotAgent import RobotAgent
from HumanAgent import HumanAgent
from State import State
import random
import sys
import json

if __name__ == "__main__":
    with open("objects.json", "r") as file:
        objects = json.load(file)

    seed = 0
    #seed = random.randrange(sys.maxsize)
    #interaction = State.FirstInteraction
    interaction = State.SecondInteraction
    robot = RobotAgent(seed, interaction, len(objects), "robot1_kb.json")
    human = HumanAgent(seed, interaction, objects)
    human.connect(robot)
    robot.start()
    human.start()
    robot.join()
    human.join()
