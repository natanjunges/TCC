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
from time import time
from argparse import ArgumentParser
import os

if __name__ == "__main__":
    parser = ArgumentParser(description= "TCC - Software part of my undergraduate thesis in Computer Engineering at the Federal University of Technology – Parana (UTFPR), Brazil.")
    parser.add_argument("--robot-ids", "-I", type= int, metavar= "ID", nargs="+", required= True)
    parser.add_argument("--path-prefix", "-p", type= os.path.abspath, metavar= "PREFIX", default= "./data")
    parser.add_argument("--seed", "-s", type= float, default= time())
    parser.add_argument("--noise", "-n", type= float, default= 0.1)
    parser.add_argument("--interaction", "-i", type= State.__getitem__, choices= [State.FirstInteraction, State.SecondInteraction], metavar= "{FirstInteraction, SecondInteraction}", required= True)
    parser.add_argument("--initial-state", "-S", type= State.__getitem__, choices= [State.TR, State.TIR], metavar= "{TR, TIR}")
    parser.add_argument("--patch-model", "-m", action= "store_true")
    parser.add_argument("--evaluate-only", "-e", action= "store_true")
    parser.add_argument("--rounds", "-r", type= int, required= True)
    args = parser.parse_args()
    args.patch_model = args.interaction == State.SecondInteraction and args.patch_model
    run = "-I {} -p \"{}\" -s {} -n {} -i {}".format(" ".join([str(id) for id in args.robot_ids]), args.path_prefix, args.seed, args.noise, "FirstInteraction" if args.interaction == State.FirstInteraction else "SecondInteraction")

    if args.initial_state is not None:
        run += " -S " + ("TR" if args.initial_state == State.TR else "TIR")

    if args.patch_model:
        run += " -m"

    if args.evaluate_only:
        run += " -e"

    run += " -r {}\n".format(args.rounds)

    with open(args.path_prefix + "/runs", "a") as file:
        file.write(run)

    with open(args.path_prefix + "/objects.json", "r") as file:
        objects = json.load(file)

    seed_generator = random.Random(args.seed)
    robots = dict()
    humans = dict()

    for id in args.robot_ids:
        if not os.path.isdir("{}/{}/".format(args.path_prefix, id)):
            os.mkdir("{}/{}/".format(args.path_prefix, id))

        seed = seed_generator.randrange(sys.maxsize)
        robots[id] = RobotAgent(id, args.path_prefix, seed, args.noise, args.interaction, len(objects), args.initial_state, args.evaluate_only)

        if args.patch_model:
            robots[id].patch_model()

        humans[id] = HumanAgent(id, args.path_prefix, seed, args.noise, args.interaction, objects, args.evaluate_only)
        humans[id].connect(robots[id])

    for i in range(args.rounds):
        print("robot ids: {}".format(args.robot_ids))
        print("path prefix: " + args.path_prefix)
        print("run seed: {}".format(args.seed))

        if args.patch_model:
            print("patch model")

        if args.evaluate_only:
            print("evaluate only")

        print("round: {}/{}".format(i + 1, args.rounds))

        for id in args.robot_ids:
            robots[id].start()
            humans[id].start()

        for id in args.robot_ids:
            robots[id].join()
            humans[id].join()
            seed = seed_generator.randrange(sys.maxsize)
            robots[id].reset(seed= seed)
            humans[id].reset(seed= seed)

        os.system("clear")

    print("robot ids: {}".format(args.robot_ids))
    print("path prefix: " + args.path_prefix)
    print("run seed: {}".format(args.seed))

    if args.patch_model:
        print("patch model")

    if args.evaluate_only:
        print("evaluate only")

    print("rounds: {}".format(args.rounds))
