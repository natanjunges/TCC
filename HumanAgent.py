from Agent import Agent
from State import State
import random

class HumanAgent(Agent):
    def __init__(self, objects):
        kb = {(object_index, word) for object_index, object in zip(range(len(objects)), objects) for word in object}
        super().__init__(objects, kb)

    def connect(self, agent):
        super().connect(agent)
        self.robot_state = agent.state

    def run(self):
        self.state = State.TR
        self.logger.debug("{}#{} state: {}".format(self.__class__.__name__, self.process.pid, self.state))
        self.object_index_2 = None
        self.word_1 = None
        self.word_2 = None

        while self.running.value:
            if self.state == State.CR:
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
            elif self.state == State.End:
                self.running.value = False
                break

            self.wait()
            self.state = State(self.robot_state.value)
            self.logger.debug("{}#{} state: {}".format(self.__class__.__name__, self.process.pid, self.state))
            self.wait()

    def RRC1(self):
        self.object_index_2 = int(self.recv())
        self.send(str(self.object_index_2) + "?")

    def TW(self):
        self.word_1 = random.choice([word for object_index, word in self.kb if object_index == self.object_index_2])
        self.send(self.word_1)

    def RWC2(self):
        self.word_2 = self.recv().rstrip("?")

        if self.word_1 == self.word_2:
            self.state = State.CW1
        else:
            self.state = State.TW

    def CW1(self):
        self.send("True")
