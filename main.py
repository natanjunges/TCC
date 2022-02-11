#!/usr/bin/env python3

from RobotAgent import RobotAgent
from HumanAgent import HumanAgent
from time import sleep

if __name__ == "__main__":
    objects = []
    robot = RobotAgent(objects)
    human = HumanAgent(objects)
    human.connect(robot)
    robot.start()
    human.start()
    sleep(5)
    robot.stop()
    human.stop()
