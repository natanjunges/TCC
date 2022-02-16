from Agent import Agent
from State import State
import random
from multiprocessing import Value

class RobotAgent(Agent):
    def __init__(self, objects, kb= None):
        super().__init__(objects, kb)
        self.state = Value("i", State.Start.value)

    def run(self):
        self.state.value = State.TR.value
        self.logger.debug("{}#{} state: {}".format(self.__class__.__name__, self.process.pid, State(self.state.value)))
        self.object_index_1 = None
        self.object_index_2 = None
        self.word_2 = None

        while self.running.value:
            state = self.state.value

            if state in {State.RRC1.value, State.TW.value, State.RWC2.value}:
                self.wait()
            elif state == State.TR.value:
                self.TR()
            elif state == State.RRC2.value:
                self.RRC2()
            elif state == State.CR.value:
                self.CR()
            elif state == State.RWC1.value:
                self.RWC1()
            elif state == State.CW2.value:
                self.CW2()
            elif state == State.End.value:
                self.running.value = False
                break

            if state != State.RRC2.value:
                # decide next state

                if state == State.TR.value:
                    self.state.value = State.RRC1.value
                elif state == State.RRC1.value:
                    self.state.value = State.RRC2.value
                elif state == State.CR.value:
                    self.state.value = State.TW.value
                elif state == State.TW.value:
                    self.state.value = State.RWC1.value
                elif state == State.RWC1.value:
                    self.state.value = State.RWC2.value
                elif state == State.RWC2.value:
                    self.recv()
                    self.state.value = State.CW2.value
                elif state == State.CW2.value:
                    self.state.value = State.End.value

            self.logger.debug("{}#{} state: {}".format(self.__class__.__name__, self.process.pid, State(self.state.value)))
            self.wait()
            self.wait()

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
