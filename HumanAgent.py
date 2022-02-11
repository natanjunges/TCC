from Agent import Agent
from State import State
import random

class HumanAgent(Agent):
    def connect(self, agent):
        super().connect(agent)
        self.robot_state = agent.state

    def run(self):
        self.state = State.TR
        self.object_index_2 = None
        self.word_1 = None
        self.word_2 = None
        self.kb = set()
        random.seed()

        while self.running.value:
            if self.state in {State.TR, State.RRC2, State.CR, State.RWC1}:
                self.wait()
            elif self.state == State.RRC1:
                self.RRC1()
            elif self.state == State.TW:
                self.TW()
            elif self.state == State.RWC2:
                self.RWC2()
                continue
            elif self.state == State.CW1:
                self.CW1()
            elif self.state == State.End:
                self.running.value = False
                break

            self.state = State(self.robot_state.value)

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
