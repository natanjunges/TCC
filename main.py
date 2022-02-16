#!/usr/bin/env python3

from RobotAgent import RobotAgent
from HumanAgent import HumanAgent
import random

if __name__ == "__main__":
    objects = [["foo", "Foo", "f00"], ["bar", "Bar", "b4r"], ["lol", "Lol", "l0l"], ["biz", "Biz", "b1z"]]
    random.seed()
    robot = RobotAgent(objects)
    human = HumanAgent(objects)
    human.connect(robot)
    robot.start()
    human.start()
    robot.join()
    human.join()
