# This file is part of TCC
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

from .Agent import Agent
from .State import State
from .Message import Message
from .utils import insert
from learning_core.Learner import Learner
import random
from multiprocessing import Value
import os.path
import json
from shutil import copyfile
import os
import logging

class RobotAgent(Agent):
    def __init__(self, id, path_prefix, seed, noise, interaction, n_objects, batch_size, initial_state= None):
        super().__init__(id, path_prefix, seed, noise, interaction)
        self.n_objects = n_objects
        self.kb_file = "{}/robot{}_kb.json".format(self.path_prefix, self.id)
        self.initial_state = initial_state if self.interaction == State.SecondInteraction else self.interaction

        if os.path.isfile(self.kb_file):
            with open(self.kb_file, "r") as file:
                self.kb = json.load(file)
        else:
            self.kb = []

        self.model_file = "{}/robot{}_model.pddl".format(self.path_prefix, self.id)

        if not os.path.isfile(self.model_file):
            copyfile("./learning_core/model/empty-1.pddl", self.model_file)

            if self.interaction == State.SecondInteraction:
                os.system("patch \"{}\" < ./learning_core/model/empty-2.pddl.patch > /dev/null".format(self.model_file))

        self.batch_size = batch_size
        self.obs_file = "{}/tmp/robot{}_obs".format(self.path_prefix, self.id)

        self.learner = Learner(self)
        self.state = Value("i", State.Start.value)

    def reset(self, seed= None, noise= None, interaction= None, initial_state= None):
        super().reset(seed, noise, interaction)
        self.initial_state = initial_state if self.interaction == State.SecondInteraction else self.interaction
        self.state.value = State.Start.value

        if os.path.isfile(self.kb_file):
            with open(self.kb_file, "r") as file:
                self.kb = json.load(file)
        else:
            self.kb = []

        self.learner.reset()

    def accept(self, conn, barrier):
        self.conn = conn
        self.barrier = barrier

    def poll(self):
        return self.conn.poll()

    def patch_model2(self):
        os.system("patch \"{}\" < ./learning_core/model/empty-2.pddl.patch > /dev/null".format(self.model_file))
        self.learner = Learner(self)

    def possible_states(self, msg):
        msg = Message.fromString(msg)

        if msg == Message.IntegerQuestion:
            if self.interaction == State.FirstInteraction:
                return [State.RRC1]
            elif self.interaction == State.SecondInteraction:
                return [State.RRC1, State.RIRC1]
        elif msg == Message.String:
            return [State.TW]
        elif msg == Message.Boolean:
            if self.interaction == State.FirstInteraction:
                return [State.CW1]
            elif self.interaction == State.SecondInteraction:
                return [State.CW1, State.CI1]

    def guess_next_state(self, states= None):
        if states is None:
            states = [State.TR, State.RRC1, State.RRC2, State.CR, State.TW, State.RWC1, State.RWC2, State.CW1, State.CW2]

            if self.interaction == State.SecondInteraction:
                states += [State.TIR, State.RIRC1, State.RIRC2, State.CIR, State.RIC1, State.RIC2, State.CI1, State.CI2]

        if len(states) == 1:
            return states[0]
        else:
            return random.choice(self.learner.choose(states))

    def run(self):
        super().run()
        self.info("initial state: {}".format(self.initial_state))
        self.state.value = (self.initial_state if self.initial_state is not None else random.choice([State.TR, State.TIR])).value
        self.states = []
        msg = None
        state = State.Start

        while True:
            self.notify()

            try:
                self.wait()
            except:
                if self.logger.isEnabledFor(logging.INFO):
                    self.info("states: {}".format(self.states))

                self.learner.learn()
                break

            prev_state = state
            state = State(self.state.value)

            if self.poll():
                msg = self.recv()
                states = self.possible_states(msg)

                if self.logger.isEnabledFor(logging.DEBUG):
                    self.debug("possible states: {}".format(states))

                if (State.TW in states and prev_state != State.CR or State.CW1 in states) and state in {State.RWC2, State.RIC2}:
                    self.notify()

                    try:
                        self.wait()
                    except:
                        if self.logger.isEnabledFor(logging.INFO):
                            self.info("states: {}".format(self.states))

                        self.learner.learn()
                        break

                    self.debug("state: {}".format(state))
                    self.learner.add_action(state)
                    self.states.append(state)

                state = self.guess_next_state(states)
                self.debug("guessed state: {}".format(state))
                self.state.value = state.value
                self.notify()

                try:
                    self.wait()
                except:
                    if self.logger.isEnabledFor(logging.INFO):
                        self.info("states: {}".format(self.states))

                    self.learner.learn()
                    break

                self.learner.add_action(state)

                if state in {State.RRC1, State.RIRC1}:
                    self.object_index_2 = None
                    self.word = None
                elif state == State.TW:
                    self.word = None

                self.learner.add_state(None, Message.fromString(msg))

                if state in {State.CW1, State.CI1}:
                    self.learner.add_state(None, None)
                    msg = None
            elif state == State.TR:
                self.TR()
                self.learner.add_action(state)
                self.learner.add_state(Message.Integer, Message.fromString(msg) if msg is not None else None)
            elif state == State.RRC2:
                self.RRC2(msg)
                self.learner.add_action(state)
                self.learner.add_state(None, None)
                msg = None
            elif state == State.CR:
                self.CR()
                self.learner.add_action(state)
                self.learner.add_state(Message.Boolean, Message.fromString(msg) if msg is not None else None)
            elif state == State.RWC1:
                self.RWC1(msg)
                self.learner.add_action(state)
                self.learner.add_state(Message.StringQuestion, None)
                msg = None
            elif state == State.CW2:
                self.CW2()
                self.learner.add_action(state)
                self.learner.add_state(None, Message.fromString(msg) if msg is not None else None)
            elif state == State.TIR:
                self.TIR()
                self.learner.add_action(state)
                self.learner.add_state(Message.Integer, Message.fromString(msg) if msg is not None else None)
            elif state == State.RIRC2:
                self.RIRC2(msg)
                self.learner.add_action(state)
                self.learner.add_state(None, None)
                msg = None
            elif state == State.CIR:
                self.CIR()
                self.learner.add_action(state)
                self.learner.add_state(Message.Boolean, Message.fromString(msg) if msg is not None else None)
            elif state == State.RIC1:
                self.RIC1()
                self.learner.add_action(state)
                self.learner.add_state(Message.StringQuestion, Message.fromString(msg) if msg is not None else None)
            elif state == State.CI2:
                self.CI2()
                self.learner.add_action(state)
                self.learner.add_state(None, Message.fromString(msg) if msg is not None else None)
            elif state == State.End:
                if self.logger.isEnabledFor(logging.INFO):
                    self.info("states: {}".format(self.states))

                self.learner.learn()
                break

            self.debug("state: {}".format(state))
            self.states.append(state)

            if state in {State.CW2, State.CI2}:
                self.state.value = State.End.value
            elif state not in {State.RRC2, State.RIRC2}:
                self.state.value = self.guess_next_state().value

            self.debug("guessed state: {}".format(State(self.state.value)))

    def TR(self):
        if self.object_index_1 is None:
            self.object_index_1 = random.randrange(self.n_objects)

        self.object_index_2 = None
        self.word = None
        self.send(str(self.object_index_1))

    def RRC2(self, msg):
        self.object_index_2 = int(msg.rstrip("?"))
        self.word = None

        if self.object_index_1 == self.object_index_2:
            self.state.value = State.CR.value
        else:
            self.state.value = State.TR.value

    def CR(self):
        self.send("True")

    def RWC1(self, msg):
        self.word = msg

        if self.noise >= 1 or self.noise > 0 and random.random() < self.noise:
            x = random.randrange(len(self.word))
            self.word = self.word[:x] + self.word[x + 1:]

        self.send(self.word + "?")

    def CW2(self):
        if insert(self.kb, [self.object_index_1, self.word]):
            if self.logger.isEnabledFor(logging.DEBUG):
                self.debug("kb: {}".format(self.kb))

            with open(self.kb_file, "w") as file:
                json.dump(self.kb, file)

        self.object_index_1 = None
        self.object_index_2 = None
        self.word = None

    def TIR(self):
        if self.object_index_1 is None:
            self.object_index_1 = random.randrange(self.n_objects)

        self.object_index_2 = None
        self.word = None
        self.send(str(self.object_index_1))

    def RIRC2(self, msg):
        self.object_index_2 = int(msg.rstrip("?"))
        self.word = None

        if self.object_index_1 == self.object_index_2:
            self.state.value = State.CIR.value
        else:
            self.state.value = State.TIR.value

    def CIR(self):
        self.send("True")

    def RIC1(self):
        if self.word is None:
            self.word = random.choice(sorted({word for _, word in self.kb}))

        self.send(self.word + "?")

    def CI2(self):
        if insert(self.kb, [self.object_index_1, self.word]):
            if self.logger.isEnabledFor(logging.DEBUG):
                self.debug("kb: {}".format(self.kb))

            with open(self.kb_file, "w") as file:
                json.dump(self.kb, file)

        self.object_index_1 = None
        self.object_index_2 = None
        self.word = None
