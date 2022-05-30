#!/usr/bin/env python3

# TCC - Software part of my undergraduate thesis in Computer Engineering
# at the Federal University of Technology – Parana (UTFPR), Brazil.
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

import random
import sys
import json
from time import time
from argparse import ArgumentParser
import os

from agent_core.RobotAgent import RobotAgent
from agent_core.HumanAgent import HumanAgent
from agent_core.State import State

if __name__ == "__main__":
    parser = ArgumentParser(description="TCC - Software part of my "
                            "undergraduate thesis in Computer Engineering at "
                            "the Federal University of Technology – Parana "
                            "(UTFPR), Brazil.")
    parser.add_argument("--robot-ids", "-I", type=int, metavar="ID", nargs="+",
                        required=True,
                        help="IDs of robots to be executed in parallel")
    # Gets the absolute path of the path prefix so it is independent of
    # where it runs from.
    parser.add_argument("--path-prefix", "-p", type=os.path.abspath,
                        metavar="PREFIX", default="./data",
                        help="where all data will be loaded from/stored to")
    parser.add_argument("--seed", "-s", type=float, default=time(),
                        help="master seed that generates seeds for each run")
    parser.add_argument("--noise", "-n", type=float, default=0.1,
                        help="probability of noise in exchanged messages")
    # Converts the string to a State enum.
    parser.add_argument("--interaction", "-i", type=State.__getitem__,
                        choices=[State.FirstInteraction,
                                 State.SecondInteraction],
                        metavar="{FirstInteraction, SecondInteraction}",
                        required=True,
                        help="which part of the experiment to run")
    # Converts the string to a State enum.
    parser.add_argument("--initial-state", "-S", type=State.__getitem__,
                        choices=[State.TR, State.TIR], metavar="{TR, TIR}",
                        help="initial state of agents in 2nd interaction")
    parser.add_argument("--patch-model", "-m", action="store_true",
                        help="adds actions required in 2nd interaction")
    parser.add_argument("--evaluate-only", "-e", action="store_true",
                        help="doesn't update model")
    parser.add_argument("--rounds", "-r", type=int, required=True,
                        help="how many runs to execute each robot")
    args = parser.parse_args()
    # Ignores the patch model argument if not in the 2nd interaction.
    args.patch_model = (args.interaction == State.SecondInteraction
                        and args.patch_model)
    # Logs the used arguments for reproducibility.
    run = "-I {} -p \"{}\" -s {} -n {} -i {}".format(
        " ".join([str(id) for id in args.robot_ids]),
        args.path_prefix, args.seed, args.noise,
        "FirstInteraction" if args.interaction == State.FirstInteraction
        else "SecondInteraction")

    if args.initial_state is not None:
        run += " -S " + ("TR" if args.initial_state == State.TR else "TIR")

    if args.patch_model:
        run += " -m"

    if args.evaluate_only:
        run += " -e"

    run += " -r {}\n".format(args.rounds)

    with open(args.path_prefix + "/runs", "a") as file:
        file.write(run)

    # Loads the environment model used in the experiment.
    with open(args.path_prefix + "/objects.json", "r") as file:
        objects = json.load(file)

    seed_generator = random.Random(args.seed)
    robots = dict()
    humans = dict()

    for id in args.robot_ids:
        # Initializes the robot's folder.
        if not os.path.isdir("{}/{}/".format(args.path_prefix, id)):
            os.mkdir("{}/{}/".format(args.path_prefix, id))

        seed = seed_generator.randrange(sys.maxsize)
        robots[id] = RobotAgent(id, args.path_prefix, seed, args.noise,
                                args.interaction, len(objects),
                                args.initial_state, args.evaluate_only)

        if args.patch_model:
            robots[id].patch_model()

        humans[id] = HumanAgent(id, args.path_prefix, seed, args.noise,
                                args.interaction, objects, args.evaluate_only)
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
            # Gets the agents ready for the next round.
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
