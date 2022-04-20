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
from .utils import insert, merge, sub
from multiprocessing import Pipe, Barrier
import json
import os.path
from datetime import datetime

class HumanAgent(Agent):
    def __init__(self, id, path_prefix, seed, noise, interaction, objects):
        super().__init__(id, path_prefix, seed, noise, interaction)
        self.objects = objects
        self.log_file = "{}/{}/log.json".format(self.path_prefix, self.id)

    def reset(self, seed= None, noise= None, interaction= None):
        super().reset(seed, noise, interaction)
        self.state = State.Start
        self.barrier.reset()

    def connect(self, agent):
        self_conn, agent_conn = Pipe()
        self.conn = self_conn
        self.barrier = Barrier(2)
        self.robot_state = agent.state
        agent.accept(agent_conn, self.barrier)

    def abort(self):
        self.barrier.abort()
        self.log(self.SYNCHRONIZATION, "aborted")

    def can_be_next(self, state, next_state):
        # Legal state transitions for FirstInteraction (22):
        # TR, RRC1
        # RRC1, TR
        # RRC1, RRC2
        # RRC1, TW
        # RRC2, TR
        # RRC2, CR
        # CR, TW
        # TW, TR
        # TW, CR
        # TW, TW
        # TW, RWC1
        # TW, CW2
        # RWC1, TW
        # RWC1, RWC2
        # RWC1, CW1
        # RWC2, TW
        # RWC2, CW1
        # CW1, TR
        # CW1, CR
        # CW1, TW
        # CW1, CW1
        # CW1, CW2
        # Legal state transitions for SecondInteraction (70):
        # TR, RRC1
        # TR, RIRC1
        # RRC1, TR
        # RRC1, RRC2
        # RRC1, TW
        # RRC1, TIR
        # RRC1, RIRC2
        # RRC1, RIC1
        # RRC2, TR
        # RRC2, CR
        # CR, TW
        # TW, TR
        # TW, CR
        # TW, TW
        # TW, RWC1
        # TW, CW2
        # TW, TIR
        # TW, CIR
        # TW, RIC1
        # TW, CI2
        # RWC1, TW
        # RWC1, RWC2
        # RWC1, CW1
        # RWC2, TW
        # RWC2, CW1
        # CW1, TR
        # CW1, CR
        # CW1, TW
        # CW1, CW1
        # CW1, CW2
        # CW1, TIR
        # CW1, CIR
        # CW1, RIC1
        # CW1, CI1
        # CW1, CI2
        # TIR, RRC1
        # TIR, RIRC1
        # RIRC1, TR
        # RIRC1, RRC2
        # RIRC1, TW
        # RIRC1, TIR
        # RIRC1, RIRC2
        # RIRC1, RIC1
        # RIRC2, TIR
        # RIRC2, CIR
        # CIR, TR
        # CIR, CR
        # CIR, TW
        # CIR, CW1
        # CIR, CW2
        # CIR, TIR
        # CIR, CIR
        # CIR, RIC1
        # CIR, CI1
        # CIR, CI2
        # RIC1, TW
        # RIC1, RIC2
        # RIC1, CI1
        # RIC2, TW
        # RIC2, CI1
        # CI1, TR
        # CI1, CR
        # CI1, TW
        # CI1, CW1
        # CI1, CW2
        # CI1, TIR
        # CI1, CIR
        # CI1, RIC1
        # CI1, CI1
        # CI1, CI2

        if next_state == State.TR:
            return state in {State.Start, State.RRC1, State.RRC2, State.TW, State.CW1, State.RIRC1, State.CIR, State.CI1}
        elif next_state in {State.RRC1, State.RIRC1}:
            return state in {State.TR, State.TIR}
        elif next_state in {State.RRC2, State.RIRC2}:
            return state in {State.RRC1, State.RIRC1} and self.object_index_1 is not None
        elif next_state == State.CR:
            return state in {State.RRC2, State.TW, State.CW1, State.CIR, State.CI1} and self.object_index_1 is not None and self.object_index_2 is not None and self.object_index_1 == self.object_index_2
        elif next_state == State.TW:
            return state in {State.RRC1, State.CR, State.TW, State.RWC1, State.RWC2, State.CW1, State.RIRC1, State.CIR, State.RIC1, State.RIC2, State.CI1} and self.object_index is not None
        elif next_state == State.RWC1:
            return state == State.TW
        elif next_state == State.RWC2:
            return state == State.RWC1 and self.word_1 is not None
        elif next_state == State.CW1:
            return state in {State.RWC1, State.RWC2, State.CW1, State.CIR, State.CI1} and self.word_1 is not None and self.word_2 is not None and self.word_1 == self.word_2
        elif next_state in {State.CW2, State.CI2}:
            return state in {State.TW, State.CW1, State.CIR, State.CI1} and self.object_index_1 is not None and self.word is not None
        elif next_state == State.TIR:
            return state in {State.Start, State.RRC1, State.TW, State.CW1, State.RIRC1, State.RIRC2, State.CIR, State.CI1}
        elif next_state == State.CIR:
            return state in {State.TW, State.CW1, State.RIRC2, State.CIR, State.CI1} and self.object_index_1 is not None and self.object_index_2 is not None and self.object_index_1 == self.object_index_2
        elif next_state == State.RIC1:
            return state in {State.RRC1, State.TW, State.CW1, State.RIRC1, State.CIR, State.CI1}
        elif next_state == State.RIC2:
            return state == State.RIC1 and self.object_index is not None
        elif next_state == State.CI1:
            return state in {State.CW1, State.CIR, State.RIC1, State.RIC2, State.CI1} and self.object_index is not None and self.word_2 is not None and self.word_2 in self.objects[self.object_index]

    def run_state(self):
        if self.state == State.RRC1:
            self.RRC1()
        elif self.state == State.TW:
            self.TW()
        elif self.state == State.RWC2:
            self.RWC2()
            self.log(self.STATES, "state: {}".format(self.state))

            if self.state == State.TW:
                self.TW()
            elif self.state == State.CW1:
                self.CW1()
        elif self.state == State.CW1:
            self.CW1()
        elif self.state == State.RIRC1:
            self.RIRC1()
        elif self.state == State.RIC2:
            self.RIC2()
            self.log(self.STATES, "state: {}".format(self.state))

            if self.state == State.TW:
                self.TW()
            elif self.state == State.CI1:
                self.CI1()
        elif self.state == State.CI1:
            self.CI1()
        elif self.state == State.End:
            self.notify()
            return False

        return True

    def a(self, state):
        if self.interaction == State.SecondInteraction:
            if state == State.TIR:
                state = State.TR
            elif state == State.RIRC1:
                state = State.RRC1
            elif state == State.RIRC2:
                state = State.RRC2
            elif state == State.CIR:
                state = State.CR
            elif state == State.RIC1:
                state = State.RWC1
            elif state == State.RIC2:
                state = State.RWC2
            elif state == State.CI1:
                state = State.CW1
            elif state == State.CI2:
                state = State.CW2

        return 0.02 * state.value + 0.8

    def d(self):
        transitions = []
        new_transitions = self.get_transitions()

        if os.path.isfile(self.log_file):
            with open(self.log_file, "r") as file:
                for line in file:
                    interaction = json.loads(line)

                    if interaction["interaction"] == ("FirstInteraction" if self.interaction == State.FirstInteraction else "SecondInteraction"):
                        merge(transitions, [[State[transition[0]], State[transition[1]]] for transition in interaction["new_transitions"]])

                        if len(transitions) >= (22 if self.interaction == State.FirstInteraction else 70):
                            break

        sub(new_transitions, transitions)
        return (new_transitions, (0.0072 if self.interaction == State.FirstInteraction else 0.0022) * (len(transitions) + len(new_transitions)) + 0.84)

    def update_transitions(self, state, condition, legal):
        self.state_transitions += 1

        if self.state_transitions > (28 if self.interaction == State.FirstInteraction else 20) and condition:
            self.kill_robot(state, legal, False)
            return False
        else:
            return True

    def kill_robot(self, state, legal, limit):
        self.abort()
        d = self.d()
        score = self.a(state) * (1 if legal else 0.84) * (1 if limit else 0.84) * d[1]
        self.save_log(state, legal, d[0], score)

    def save_log(self, state, legal, transitions, score):
        interaction = {
            "timestamp": datetime.utcnow().isoformat(" "),
            "seed": self.seed,
            "noise": self.noise,
            "interaction": "FirstInteraction" if self.interaction == State.FirstInteraction else "SecondInteraction",
            "initial_state": str(self.initial_state),
            "last_state": str(state),
            "legal_transition": legal,
            "n_transitions": self.state_transitions,
            "new_transitions": [[str(transition[0]), str(transition[1])] for transition in transitions],
            "score": score
        }

        with open(self.log_file, "a") as file:
            file.write(json.dumps(interaction) + "\n")

        if self.logger.isEnabledFor(self.SIMULATION):
            self.log(self.SIMULATION, "last state: {}".format(state))
            self.log(self.SIMULATION, "legal transition: {}".format(legal))
            self.log(self.SIMULATION, "number of transitions: {}".format(self.state_transitions))
            self.log(self.SIMULATION, "new transitions: {}".format(transitions))
            self.log(self.SIMULATION, "score: {}".format(score))

    def get_transitions(self):
        i = 0
        l = len(self.states) - 1
        transitions = []

        while i < l:
            insert(transitions, [self.states[i], self.states[i + 1]])
            i += 1

        return transitions

    def sync_state(self, prev_state):
        self.notify_wait()
        state = State(self.robot_state.value)

        if self.can_be_next(prev_state, state):
            self.state = state
            self.states.append(state)
            self.log(self.STATES, "synced state: {}".format(self.state))

            if self.state in {State.RWC2, State.RIC2}:
                prev_state = state
                self.notify_wait()
                state = State(self.robot_state.value)
                cbn = self.can_be_next(prev_state, state)

                if not self.update_transitions(state, True, cbn):
                    return None

                if cbn:
                    self.state = state
                    self.states.append(state)
                    self.log(self.STATES, "synced state: {}".format(self.state))
                else:
                    self.kill_robot(state, False, True)
                    return None

            return prev_state
        else:
            self.kill_robot(state, False, True)
            return None

    def run(self):
        super().run()
        self.object_index = None
        self.word_1 = None
        self.word_2 = None
        self.state_transitions = -1
        self.initial_state = None
        self.states = []
        state = State.Start
        self.wait()

        while True:
            if self.state in {State.CR, State.CIR}:
                self.recv()

            prev_state = state
            state = State(self.robot_state.value)

            if not self.update_transitions(state, self.state not in {State.CW2, State.CI2}, self.can_be_next(self.state, state)):
                if self.logger.isEnabledFor(self.STATES):
                    self.log(self.STATES, "states: {}".format(self.states))

                break

            if self.state in {State.TR, State.CR, State.RWC1, State.CW2, State.TIR, State.RIC1, State.CI2}:
                if self.state == State.TR:
                    self.object_index_2 = None
                    self.word = None
                    self.state = State.RRC1
                elif self.state == State.CR:
                    self.state = State.TW
                elif self.state == State.RWC1:
                    self.state = State.RWC2
                elif self.state == State.TIR:
                    self.object_index_2 = None
                    self.word = None
                    self.state = State.RIRC1
                elif self.state == State.RIC1:
                    self.state = State.RIC2
                elif self.state in {State.CW2, State.CI2}:
                    self.object_index_1 = None
                    self.object_index_2 = None
                    self.word = None
                    self.state = State.End

                self.log(self.STATES, "state: {}".format(self.state))

                if not self.run_state():
                    if self.logger.isEnabledFor(self.STATES):
                        self.log(self.STATES, "states: {}".format(self.states))

                    break

                prev_state = self.sync_state(prev_state)

                if prev_state is not None:
                    state = self.state
                else:
                    if self.logger.isEnabledFor(self.STATES):
                        self.log(self.STATES, "states: {}".format(self.states))

                    break
            else:
                if self.state in {State.RRC2, State.RIRC2}:
                    self.object_index_2 = self.object_index
                    self.word = None

                if self.can_be_next(self.state, state):
                    self.state = state
                    self.log(self.STATES, "state: {}".format(self.state))

                    if self.initial_state is None:
                        self.initial_state = self.state

                    if self.state in {State.RRC1, State.TW, State.RWC2, State.CW1, State.RIRC1, State.RIC2, State.CI1}:
                        self.run_state()
                        prev_state = self.sync_state(prev_state)

                        if prev_state is not None:
                            state = self.state
                        else:
                            if self.logger.isEnabledFor(self.STATES):
                                self.log(self.STATES, "states: {}".format(self.states))

                            break
                    else:
                        self.states.append(state)

                        if self.state in {State.CW2, State.CI2}:
                            d = self.d()
                            self.save_log(self.state, True, d[0], d[1])
                else:
                    self.kill_robot(state, False, True)

                    if self.logger.isEnabledFor(self.STATES):
                        self.log(self.STATES, "states: {}".format(self.states))

                    break

            self.notify_wait()

    def RRC1(self):
        self.object_index = int(self.recv())
        self.object_index_1 = self.object_index
        self.object_index_2 = None
        self.word = None
        self.word_1 = None
        self.word_2 = None

        if self.noise >= 1 or self.noise > 0 and self.random.random() < self.noise:
            self.object_index = self.random.choice([self.object_index - 1 if self.object_index > 0 else self.object_index, self.object_index + 1 if self.object_index < len(self.objects) - 1 else self.object_index])

        self.send("{}?".format(self.object_index))

    def TW(self):
        if self.word_1 is None:
            self.word_1 = self.random.choice(self.objects[self.object_index])

        self.word = None
        self.word_2 = None
        self.send(self.word_1)

    def RWC2(self):
        self.word_2 = self.recv().rstrip("?")
        self.word = self.word_2

        if self.word_1 == self.word_2:
            self.state = State.CW1
        else:
            self.state = State.TW

    def CW1(self):
        self.send("True")

    def RIRC1(self):
        self.object_index = int(self.recv())
        self.object_index_1 = self.object_index
        self.object_index_2 = None
        self.word = None
        self.word_1 = None
        self.word_2 = None

        if self.noise >= 1 or self.noise > 0 and self.random.random() < self.noise:
            self.object_index = self.random.choice([self.object_index - 1 if self.object_index > 0 else self.object_index, self.object_index + 1 if self.object_index < len(self.objects) - 1 else self.object_index])

        self.send("{}?".format(self.object_index))

    def RIC2(self):
        self.word_2 = self.recv().rstrip("?")
        self.word = self.word_2
        self.word_1 = None

        if self.word_2 in self.objects[self.object_index]:
            self.state = State.CI1
        else:
            self.state = State.TW

    def CI1(self):
        self.send("True")
