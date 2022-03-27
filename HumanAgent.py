from Agent import Agent
from State import State
from utils import insert, merge, sub
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
        self.barrier.abort()
        self.info("aborted")

    def can_be_next(self, state, next_state):
        # Legal state transitions for FirstInteraction (21):
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
        #     TW
        #     RWC2
        #     CW1
        # RWC2
        #     TW
        #     CW1
        # CW1
        #     TR
        #     CR
        #     TW
        #     CW1
        #     CW2
        # Legal state transitions for SecondInteraction (68):
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
        #     TW
        #     RWC2
        #     CW1
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
        #     TW
        #     RIC2
        #     CI1
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

        if state in {State.RRC2, State.RIRC2} or next_state in {State.TR, State.TIR, State.RIC1}:
            return True
        elif next_state in {State.RRC1, State.RIRC1}:
            return state in {State.TR, State.TIR}
        elif next_state in {State.RRC2, State.RIRC2}:
            return state in {State.RRC1, State.RIRC1} and self.object_index_1 != None
        elif next_state in {State.CR, State.CIR}:
            return self.object_index_1 != None and self.object_index_2 != None and self.object_index_1 == self.object_index_2
        elif next_state == State.TW:
            return self.object_index != None
        elif next_state == State.RWC1:
            return state == State.TW
        elif next_state == State.RWC2:
            return state == State.RWC1 and self.word_1 != None
        elif next_state == State.CW1:
            return self.word_1 != None and self.word_2 != None and self.word_1 == self.word_2
        elif next_state in {State.CW2, State.CI2}:
            return self.object_index_1 != None and self.word != None
        elif next_state == State.RIC2:
            return state == State.RIC1 and self.object_index != None
        elif next_state == State.CI1:
            return self.word_2 != None and self.object_index != None and self.word_2 in self.objects[self.object_index]

    def run_state(self):
        if self.state == State.RRC1:
            self.RRC1()
        elif self.state == State.TW:
            self.TW()
        elif self.state == State.RWC2:
            self.RWC2()
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
            self.debug("state: {}".format(self.state))

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
                log = json.load(file)

            for interaction in log:
                if interaction["interaction"] == ("FirstInteraction" if self.interaction == State.FirstInteraction else "SecondInteraction"):
                    merge(transitions, [[State[transition[0]], State[transition[1]]] for transition in interaction["new_transitions"]])

        sub(new_transitions, transitions)
        self.debug("visited transitions: {}".format(transitions))
        return (new_transitions, (0.0076 if self.interaction == State.FirstInteraction else 0.0023) * (len(transitions) + len(new_transitions)) + 0.84)

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
            "initial_state": str(self.initial_state),
            "last_state": str(state),
            "legal_transition": legal,
            "n_transitions": self.state_transitions,
            "new_transitions": [[str(transition[0]), str(transition[1])] for transition in transitions],
            "score": score
        }
        log.append(interaction)

        with open(self.log_file, "w") as file:
            json.dump(log, file)

        self.info("last state: {}".format(state))
        self.info("legal transition: {}".format(legal))
        self.info("number of transitions: {}".format(self.state_transitions))
        self.info("new transitions: {}".format(transitions))
        self.info("score: {}".format(score))

    def get_transitions(self):
        i = 0
        l = len(self.states) - 1
        transitions = []

        while i < l:
            insert(transitions, [self.states[i], self.states[i + 1]])
            i += 1

        return transitions

    def sync_state(self, prev_state):
        self.notify()
        self.wait()
        state = State(self.robot_state.value)

        if self.can_be_next(prev_state, state):
            self.state = state
            self.states.append(state)
            self.debug("synced state: {}".format(self.state))

            if self.state in {State.RWC2, State.RIC2}:
                prev_state = state
                self.notify()
                self.wait()
                state = State(self.robot_state.value)
                cbn = self.can_be_next(prev_state, state)

                if not self.update_transitions(state, True, cbn):
                    return None

                if cbn:
                    self.state = state
                    self.states.append(state)
                    self.debug("synced state: {}".format(self.state))
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

        while True:
            self.wait()

            if self.state in {State.CR, State.CIR}:
                self.recv()

            prev_state = state
            state = State(self.robot_state.value)

            if not self.update_transitions(state, self.state not in {State.CW2, State.CI2}, self.can_be_next(self.state, state)):
                self.debug("states: {}".format(self.states))
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
                    self.debug("states: {}".format(self.states))
                    break

                prev_state = self.sync_state(prev_state)

                if prev_state != None:
                    state = self.state
                else:
                    self.debug("states: {}".format(self.states))
                    break
            else:
                if self.state in {State.RRC2, State.RIRC2}:
                    self.object_index_2 = self.object_index
                    self.word = None

                if self.can_be_next(self.state, state):
                    self.state = state
                    self.debug("state: {}".format(self.state))

                    if self.initial_state == None:
                        self.initial_state = self.state

                    if self.state in {State.RRC1, State.TW, State.RWC2, State.CW1, State.RIRC1, State.RIC2, State.CI1}:
                        if not self.run_state():
                            self.debug("states: {}".format(self.states))
                            break

                        prev_state = self.sync_state(prev_state)

                        if prev_state != None:
                            state = self.state
                        else:
                            self.debug("states: {}".format(self.states))
                            break
                    else:
                        self.states.append(state)

                        if self.state in {State.CW2, State.CI2}:
                            d = self.d()
                            self.save_log(self.state, True, d[0], d[1])
                else:
                    self.kill_robot(state, False, True)
                    self.debug("states: {}".format(self.states))
                    break

            self.notify()

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
