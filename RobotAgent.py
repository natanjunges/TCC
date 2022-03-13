from Agent import Agent
from State import State
from Message import Message
import random
from multiprocessing import Value
import os.path
import json

class RobotAgent(Agent):
    def __init__(self, seed, noise, interaction, n_objects, kb_file= None):
        super().__init__(seed, noise)
        self.interaction = interaction
        self.n_objects = n_objects
        self.kb_file = kb_file

        if kb_file != None and os.path.isfile(kb_file):
            with open(kb_file, "r") as file:
                self.kb = {(object_index, word) for object_index, word in json.load(file)}
        else:
            self.kb = set()

        self.state = Value("i", State.Start.value)

    def accept(self, conn, barrier):
        self.conn = conn
        self.barrier = barrier

    def poll(self):
        return self.conn.poll()

    def m2s(self, msg):
        msg = Message.fromString(msg)

        if msg == Message.IntegerQuestion:
            if self.interaction == State.FirstInteraction:
                return {State.RRC1}
            else:
                return {State.RRC1, State.RIRC1}
        elif msg == Message.String:
            return {State.TW}
        elif msg == Message.Boolean:
            if self.interaction == State.FirstInteraction:
                return {State.CW1}
            else:
                return {State.CW1, State.CI1}

    def run(self):
        random.seed(self.seed)
        self.info("seed: {}".format(self.seed))
        self.debug("state: {}".format(State(self.state.value)))
        self.state.value = self.interaction.value
        self.debug("state: {}".format(self.interaction))
        self.object_index_1 = None
        self.object_index_2 = None
        self.word = None
        msg = None

        while self.running.value:
            self.wait()

            try:
                self.wait()
            except:
                self.running.value = False
                break

            state = State(self.state.value)

            if self.poll():
                msg = self.recv()
                states = self.m2s(msg)
                self.debug("possible states: {}".format(states))
                # state = guess_next_state(state, states)

                if len(states) == 1:
                    state = states.pop()
                else:
                    if State.RRC1 in states and state == State.TR:
                        state = State.RRC1
                    elif State.RIRC1 in states and state == State.TIR:
                        state = State.RIRC1
                    elif State.CW1 in states and state == State.RWC2:
                        state = State.CW1
                    elif State.CI1 in states and state == State.RIC2:
                        state = State.CI1

                self.debug("state: {}".format(state))
            elif state == State.TR:
                self.TR()
            elif state == State.RRC2:
                self.RRC2(msg)
                msg = None
            elif state == State.CR:
                self.CR()
            elif state == State.RWC1:
                self.RWC1(msg)
                msg = None
            elif state == State.CW2:
                self.CW2()
            elif state == State.TIR:
                self.TIR()
            elif state == State.RIRC2:
                self.RIRC2(msg)
                msg = None
            elif state == State.CIR:
                self.CIR()
            elif state == State.RIC1:
                self.RIC1()
            elif state == State.CI2:
                self.CI2()
            elif state == State.End:
                self.running.value = False
                break

            if state in {State.CW2, State.CI2}:
                self.state.value = State.End.value
            elif state not in {State.RRC2, State.RIRC2}:
                # self.state.value = guess_next_state(state)

                if state == State.TR:
                    self.state.value = State.RRC1.value
                elif state == State.RRC1:
                    self.state.value = State.RRC2.value
                elif state == State.CR:
                    self.state.value = State.TW.value
                elif state == State.TW:
                    self.state.value = State.RWC1.value
                elif state == State.RWC1:
                    self.state.value = State.RWC2.value
                elif state == State.CW1:
                    self.state.value = State.CW2.value
                elif state == State.TIR:
                    self.state.value = State.RIRC1.value
                elif state == State.RIRC1:
                    self.state.value = State.RIRC2.value
                elif state == State.CIR:
                    self.state.value = State.RIC1.value
                elif state == State.RIC1:
                    self.state.value = State.RIC2.value
                elif state == State.CI1:
                    self.state.value = State.CI2.value

            self.debug("state: {}".format(State(self.state.value)))

    def TR(self):
        if self.object_index_1 == None:
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
            self.word = "{}{}".format(self.word[:x], self.word[x + 1:])

        self.send("{}?".format(self.word))

    def CW2(self):
        self.kb.add((self.object_index_1, self.word))
        self.debug("kb: {}".format(self.kb))

        if self.kb_file != None:
            with open(self.kb_file, "w") as file:
                json.dump(sorted(self.kb), file)

        self.object_index_1 = None
        self.object_index_2 = None
        self.word = None

    def TIR(self):
        if self.object_index_1 == None:
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
        if self.word == None:
            self.word = random.choice(sorted({word for _, word in self.kb}))

        self.send("{}?".format(self.word))

    def CI2(self):
        self.kb.add((self.object_index_1, self.word))
        self.debug("kb: {}".format(self.kb))

        if self.kb_file != None:
            with open(self.kb_file, "w") as file:
                json.dump(sorted(self.kb), file)

        self.object_index_1 = None
        self.object_index_2 = None
        self.word = None
