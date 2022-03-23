from Agent import Agent
from State import State
import random
from multiprocessing import Pipe, Barrier
import json
import os.path
from datetime import datetime

class HumanAgent(Agent):
    def __init__(self, id, path_prefix, seed, noise, interaction, objects):
        super().__init__(id, path_prefix, seed, noise, interaction)
        self.objects = objects
        self.log_file = "{}/robot{}_log.json".format(self.path_prefix, self.id)

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
        self.info("aborted")
        self.barrier.abort()

    def can_be_next(self, next_state):
        # Legal state transitions for FirstInteraction (19):
        # TR
        #     RRC1
        # RRC1
        #     TR
        #     RRC2
        #     TW
        # RRC2
        #     TR
        #     CR
        # CR
        #     TW
        # TW
        #     TR
        #     CR
        #     TW
        #     RWC1
        # RWC1
        #     RWC2
        # RWC2
        #     TW
        #     CW1
        # CW1
        #     TR
        #     CR
        #     TW
        #     CW1
        #     CW2
        # Legal state transitions for SecondInteraction (64):
        # TR
        #     RRC1
        #     RIRC1
        # RRC1
        #     TR
        #     RRC2
        #     TW
        #     TIR
        #     RIRC2
        #     RIC1
        # RRC2
        #     TR
        #     CR
        # CR
        #     TW
        # TW
        #     TR
        #     CR
        #     TW
        #     RWC1
        #     TIR
        #     CIR
        #     RIC1
        # RWC1
        #     RWC2
        # RWC2
        #     TW
        #     CW1
        # CW1
        #     TR
        #     CR
        #     TW
        #     CW1
        #     CW2
        #     TIR
        #     CIR
        #     RIC1
        #     CI1
        #     CI2
        # TIR
        #     RRC1
        #     RIRC1
        # RIRC1
        #     TR
        #     RRC2
        #     TW
        #     TIR
        #     RIRC2
        #     RIC1
        # RIRC2
        #     TIR
        #     CIR
        # CIR
        #     TR
        #     CR
        #     TW
        #     CW1
        #     CW2
        #     TIR
        #     CIR
        #     RIC1
        #     CI1
        #     CI2
        # RIC1
        #     RIC2
        # RIC2
        #     TW
        #     CI1
        # CI1
        #     TR
        #     CR
        #     TW
        #     CW1
        #     CW2
        #     TIR
        #     CIR
        #     RIC1
        #     CI1
        #     CI2

        if self.state in {State.RRC2, State.RIRC2} or next_state in {State.TR, State.TIR, State.RIC1}:
            return True
        elif next_state in {State.RRC1, State.RIRC1}:
            return self.state in {State.TR, State.TIR}
        elif next_state in {State.RRC2, State.RIRC2}:
            return self.state in {State.RRC1, State.RIRC1} and self.object_index_1 != None
        elif next_state in {State.CR, State.CIR}:
            return self.object_index_1 != None and self.object_index_2 != None and self.object_index_1 == self.object_index_2
        elif next_state == State.TW:
            return self.object_index != None
        elif next_state == State.RWC1:
            return self.state == State.TW
        elif next_state == State.RWC2:
            return self.state == State.RWC1 and self.word_1 != None
        elif next_state == State.CW1:
            return self.word_1 != None and self.word_2 != None and self.word_1 == self.word_2
        elif next_state in {State.CW2, State.CI2}:
            return self.object_index_1 != None and self.word != None
        elif next_state == State.RIC2:
            return self.state == State.RIC1 and self.object_index != None
        elif next_state == State.CI1:
            return self.word_2 != None and self.object_index != None and self.word_2 in self.objects[self.object_index]

    def run_state(self):
        if self.state == State.RRC1:
            self.RRC1()
        elif self.state == State.TW:
            self.TW()
        elif self.state == State.RWC2:
            self.RWC2()

            if not self.update_transitions(self.state):
                return False

            self.debug("state: {}".format(self.state))

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

            if not self.update_transitions(self.state):
                return False

            self.debug("state: {}".format(self.state))

            if self.state == State.TW:
                self.TW()
            elif self.state == State.CI1:
                self.CI1()
        elif self.state == State.CI1:
            self.CI1()
        elif self.state == State.End:
            self.wait()
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

    def b(self, state):
        return 1 if self.can_be_next(state) else 0.84

    def update_transitions(self, state, condition= True, b= 1):
        self.state_transitions += 1

        if self.state_transitions > (28 if self.interaction == State.FirstInteraction else 20) and condition:
            self.abort()
            self.info("state: {}".format(state))
            self.info("transitions: {}".format(self.state_transitions))
            score = self.a(state) * b * 0.84
            self.info("score: {}".format(score))
            self.save_log(state, score)
            return False

        return True

    def save_log(self, state, score):
        if os.path.isfile(self.log_file):
            with open(self.log_file, "r") as file:
                log = json.load(file)
        else:
            log = []

        interaction = {
            "timestamp": datetime.utcnow().isoformat(" "),
            "seed": self.seed,
            "noise": self.noise,
            "interaction": "FirstInteraction" if self.interaction == State.FirstInteraction else "SecondInteraction",
            "state": str(state),
            "transitions": self.state_transitions,
            "score": score
        }
        log.append(interaction)

        with open(self.log_file, "w") as file:
            json.dump(log, file)

    def run(self):
        random.seed(self.seed)
        self.info("seed: {}".format(self.seed))
        self.debug("state: {}".format(self.state))
        self.object_index = None
        self.object_index_1 = None
        self.object_index_2 = None
        self.word = None
        self.word_1 = None
        self.word_2 = None
        self.state_transitions = -1

        while True:
            self.wait()

            if self.state in {State.CR, State.CIR}:
                self.recv()

            state = State(self.robot_state.value)

            if not self.update_transitions(state, self.state not in {State.CW2, State.CI2}, self.b(state)):
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

                self.debug("state: {}".format(self.state))

                if not self.run_state():
                    break
            else:
                if self.state in {State.RRC2, State.RIRC2}:
                    self.object_index_2 = self.object_index
                    self.word = None

                if self.can_be_next(state):
                    self.state = state
                    self.debug("state: {}".format(self.state))

                    if self.state in {State.RRC1, State.TW, State.RWC2, State.CW1, State.RIRC1, State.RIC2, State.CI1}:
                        if not self.run_state():
                            break
                    elif self.state in {State.CW2, State.CI2}:
                        self.info("transitions: {}".format(self.state_transitions))
                        self.info("score: {}".format(1.0))
                        self.save_log(self.state, 1.0)
                else:
                    self.abort()
                    self.info("state: {}".format(state))
                    self.info("transitions: {}".format(self.state_transitions))
                    score = self.a(state) * 0.84
                    self.info("score: {}".format(score))
                    self.save_log(state, score)
                    break

            self.wait()

    def RRC1(self):
        self.object_index = int(self.recv())
        self.object_index_1 = self.object_index
        self.object_index_2 = None
        self.word = None
        self.word_1 = None
        self.word_2 = None

        if self.noise >= 1 or self.noise > 0 and random.random() < self.noise:
            self.object_index = random.choice([self.object_index - 1 if self.object_index > 0 else self.object_index, self.object_index + 1 if self.object_index < len(self.objects) - 1 else self.object_index])

        self.send("{}?".format(self.object_index))

    def TW(self):
        if self.word_1 == None:
            self.word_1 = random.choice(self.objects[self.object_index])

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

        if self.noise >= 1 or self.noise > 0 and random.random() < self.noise:
            self.object_index = random.choice([self.object_index - 1 if self.object_index > 0 else self.object_index, self.object_index + 1 if self.object_index < len(self.objects) - 1 else self.object_index])

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
