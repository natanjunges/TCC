#!/usr/bin/env python3

from RobotAgent import RobotAgent
from HumanAgent import HumanAgent
import random

if __name__ == "__main__":
    objects = [["foo", "Foo", "f00", "goo", "boo"], ["bar", "Bar", "b4r", "boo", "coo"], ["lol", "Lol", "l0l", "coo", "doo"], ["biz", "Biz", "b1z", "doo", "goo"]]
    random.seed()
    robot = RobotAgent(len(objects), {(0, "goo"), (1, "boo"), (2, "coo"), (3, "doo")})
    human = HumanAgent(objects)
    human.connect(robot)
    robot.start()
    human.start()
    robot.join()
    human.join()
