#!/usr/bin/env python3

# TCC - Software part of my undergraduate thesis in Computer Engineering at the Federal University of Technology – Parana (UTFPR), Brazil.
# Copyright (C) 2022  Natan Junges <natanjunges@alunos.utfpr.edu.br>
#
# TCC is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# TCC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TCC.  If not, see <https://www.gnu.org/licenses/>.

from agent_core.RobotAgent import RobotAgent
from agent_core.HumanAgent import HumanAgent
from agent_core.State import State
import random
import sys
import json

if __name__ == "__main__":
    path_prefix = "./data"

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

    for _ in range(1000):
        robot.start()
        human.start()
        robot.join()
        human.join()
        seed = random.randrange(sys.maxsize)
        robot.reset(seed= seed)
        human.reset(seed= seed)
