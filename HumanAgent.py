from Agent import Agent
from State import State
import random

class HumanAgent(Agent):
    def __init__(self, objects):
        super().__init__()
        self.objects = objects

    def connect(self, agent):
        super().connect(agent)
        self.robot_state = agent.state

    def run(self):
        self.state = State.TIR
        self.logger.debug("{}#{} state: {}".format(self.__class__.__name__, self.process.pid, self.state))
        self.object_index = None
        self.word_1 = None
        self.word_2 = None

        while self.running.value:
            if self.state in {State.CR, State.CIR}:
                self.recv()
            elif self.state == State.RRC1:
                self.RRC1()
                self.wait()
            elif self.state == State.TW:
                self.TW()
                self.wait()
            elif self.state == State.RWC2:
                self.RWC2()
                self.logger.debug("{}#{} state: {}".format(self.__class__.__name__, self.process.pid, self.state))
                continue
            elif self.state == State.CW1:
                self.CW1()
                self.wait()
            elif self.state == State.RIRC1:
                self.RIRC1()
                self.wait()
            elif self.state == State.RIC2:
                self.RIC2()
                self.logger.debug("{}#{} state: {}".format(self.__class__.__name__, self.process.pid, self.state))
                continue
            elif self.state == State.CI1:
                self.CI1()
                self.wait()
            elif self.state == State.End:
                self.running.value = False
                break

            self.wait()
            self.state = State(self.robot_state.value)
            self.logger.debug("{}#{} state: {}".format(self.__class__.__name__, self.process.pid, self.state))
            self.wait()

    def RRC1(self):
        self.object_index = int(self.recv())
        self.word_1 = None
        self.word_2 = None
        self.send("{}?".format(self.object_index))

    def TW(self):
        if self.word_1 == None:
            self.word_1 = random.choice(self.objects[self.object_index])

        self.word_2 = None
        self.send(self.word_1)

    def RWC2(self):
        self.word_2 = self.recv().rstrip("?")

        if self.word_1 == self.word_2:
            self.state = State.CW1
        else:
            self.state = State.TW

    def CW1(self):
        self.send("True")

    def RIRC1(self):
        self.object_index = int(self.recv())
        self.word_1 = None
        self.word_2 = None
        self.send("{}?".format(self.object_index))

    def RIC2(self):
        self.word_2 = self.recv().rstrip("?")
        self.word_1 = None

        if self.word_2 in self.objects[self.object_index]:
            self.state = State.CI1
        else:
            self.state = State.TW

    def CI1(self):
        self.send("True")
