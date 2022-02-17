from Agent import Agent
from State import State
import random
from multiprocessing import Value

class RobotAgent(Agent):
    def __init__(self, n_objects, kb= None):
        super().__init__()
        self.n_objects = n_objects
        self.kb = kb if kb != None else set()
        self.state = Value("i", State.Start.value)

    def run(self):
        self.state.value = State.TIR.value
        self.logger.debug("{}#{} state: {}".format(self.__class__.__name__, self.process.pid, State(self.state.value)))
        self.object_index_1 = None
        self.object_index_2 = None
        self.word = None

        while self.running.value:
            state = self.state.value

            if state in {State.RRC1.value, State.TW.value, State.RWC2.value, State.RIRC1.value, State.RIC2.value}:
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
            elif state == State.TIR.value:
                self.TIR()
            elif state == State.RIRC2.value:
                self.RIRC2()
            elif state == State.CIR.value:
                self.CIR()
            elif state == State.RIC1.value:
                self.RIC1()
            elif state == State.CI2.value:
                self.CI2()
            elif state == State.End.value:
                self.running.value = False
                break

            if state in {State.CW2.value, State.CI2.value}:
                self.state.value = State.End.value
            elif state not in {State.RRC2.value, State.RIRC2.value}:
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
                    #self.state.value = State.RWC1.value
                    self.recv()
                    self.state.value = State.CW2.value
                elif state == State.TIR.value:
                    self.state.value = State.RIRC1.value
                elif state == State.RIRC1.value:
                    self.state.value = State.RIRC2.value
                elif state == State.CIR.value:
                    self.state.value = State.RIC1.value
                elif state == State.RIC1.value:
                    self.state.value = State.RIC2.value
                elif state == State.RIC2.value:
                    #self.state.value = State.RWC1.value
                    #self.recv()
                    #self.state.value = State.CI2.value
                    self.state.value = State.End.value

            self.logger.debug("{}#{} state: {}".format(self.__class__.__name__, self.process.pid, State(self.state.value)))
            self.wait()
            self.wait()

    def TR(self):
        if self.object_index_1 == None:
            self.object_index_1 = random.randrange(self.n_objects)

        self.object_index_2 = None
        self.word = None
        self.send(str(self.object_index_1))

    def RRC2(self):
        self.object_index_2 = int(self.recv().rstrip("?"))
        self.word = None

        if self.object_index_1 == self.object_index_2:
            self.state.value = State.CR.value
        else:
            self.state.value = State.TR.value

    def CR(self):
        self.send("True")

    def RWC1(self):
        self.word = self.recv()
        self.send("{}?".format(self.word))

    def CW2(self):
        self.kb.add((self.object_index_1, self.word))
        self.logger.debug("{}#{} kb: {}".format(self.__class__.__name__, self.process.pid, self.kb))
        self.object_index_1 = None
        self.object_index_2 = None
        self.word = None

    def TIR(self):
        if self.object_index_1 == None:
            self.object_index_1 = random.randrange(self.n_objects)

        self.object_index_2 = None
        self.word = None
        self.send(str(self.object_index_1))

    def RIRC2(self):
        self.object_index_2 = int(self.recv().rstrip("?"))
        self.word = None

        if self.object_index_1 == self.object_index_2:
            self.state.value = State.CIR.value
        else:
            self.state.value = State.TIR.value

    def CIR(self):
        self.send("True")

    def RIC1(self):
        if self.word == None:
            self.word = random.choice(list({word for _, word in self.kb}))

        self.send("{}?".format(self.word))

    def CI2(self):
        self.kb.add((self.object_index_1, self.word))
        self.logger.debug("{}#{} kb: {}".format(self.__class__.__name__, self.process.pid, self.kb))
        self.object_index_1 = None
        self.object_index_2 = None
        self.word = None
