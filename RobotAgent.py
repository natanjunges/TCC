from Agent import Agent
from State import State
import random
from multiprocessing import Value

class RobotAgent(Agent):
    def __init__(self, objects):
        super().__init__(objects)
        self.state = Value("i", 0)

    def run(self):
        self.state.value = State.TR.value
        self.object_index_1 = None
        self.object_index_2 = None
        self.word_2 = None
        self.kb = set()
        random.seed()

        while self.running.value:
            if self.state.value in {State.RRC1.value, State.TW.value, State.RWC2.value, State.CW1.value}:
                self.wait()
            elif self.state.value == State.TR.value:
                self.TR()
            elif self.state.value == State.RRC2.value:
                self.RRC2()
                continue
            elif self.state.value == State.CR.value:
                self.CR()
            elif self.state.value == State.RWC1.value:
                self.RWC1()
            elif self.state.value == State.CW2.value:
                self.CW2()
                continue
            elif self.state.value == State.End.value:
                self.running.value = False
                break

            # decide next state

    def TR(self):
        self.object_index_1 = random.randrange(len(self.objects))
        self.send(str(self.object_index_1))

    def RRC2(self):
        self.object_index_2 = int(self.recv().rstrip("?"))

        if self.object_index_1 == self.object_index_2:
            self.state.value = State.CR.value
        else:
            self.state.value = State.TR.value

    def CR(self):
        self.send("True")

    def RWC1(self):
        self.word_2 = self.recv()
        self.send(self.word_2 + "?")

    def CW2(self):
        self.kb.add((self.object_index_1, self.word_2))
        self.state.value = State.End.value
