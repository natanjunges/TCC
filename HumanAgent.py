from Agent import Agent
from State import State
import random

class HumanAgent(Agent):
    def __init__(self, seed, interaction, noise, objects):
        super().__init__(seed, interaction, noise)
        self.objects = objects

    def connect(self, agent):
        super().connect(agent)
        self.robot_state = agent.state

    def run(self):
        random.seed(self.seed)
        self.logger.info("{}#{} seed: {}".format(self.__class__.__name__, self.process.pid, self.seed))
        self.logger.debug("{}#{} state: {}".format(self.__class__.__name__, self.process.pid, self.state))
        self.object_index = None
        self.word_1 = None
        self.word_2 = None

        while self.running.value:
            self.wait()

            if self.state in {State.CR, State.CIR}:
                self.recv()

            if self.state in {State.TR, State.CR, State.RWC1, State.CW2, State.TIR, State.RIC1, State.CI2}:
                if self.state == State.TR:
                    self.state = State.RRC1
                elif self.state == State.CR:
                    self.state = State.TW
                elif self.state == State.RWC1:
                    self.state = State.RWC2
                elif self.state == State.TIR:
                    self.state = State.RIRC1
                elif self.state == State.RIC1:
                    self.state = State.RIC2
                elif self.state in {State.CW2, State.CI2}:
                    self.state = State.End

                self.logger.debug("{}#{} state: {}".format(self.__class__.__name__, self.process.pid, self.state))

                if not self.run_state():
                    break
            else:
                state = State(self.robot_state.value)

                if state in {State.RRC1, State.TW, State.RWC2, State.CW1, State.RIRC1, State.RIC2, State.CI1, State.End}:
                    #if can_be_next(self.state, state):
                        self.state = state
                        self.logger.debug("{}#{} state: {}".format(self.__class__.__name__, self.process.pid, self.state))

                        if not self.run_state():
                            break
                    #else:
                        # kill_robot
                else:
                    self.state = state
                    self.logger.debug("{}#{} state: {}".format(self.__class__.__name__, self.process.pid, self.state))

            self.wait()

    def run_state(self):
        if self.state == State.RRC1:
            self.RRC1()
        elif self.state == State.TW:
            self.TW()
        elif self.state == State.RWC2:
            self.RWC2()
            self.logger.debug("{}#{} state: {}".format(self.__class__.__name__, self.process.pid, self.state))

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
            self.logger.debug("{}#{} state: {}".format(self.__class__.__name__, self.process.pid, self.state))

            if self.state == State.TW:
                self.TW()
            elif self.state == State.CI1:
                self.CI1()
        elif self.state == State.CI1:
            self.CI1()
        elif self.state == State.End:
            self.running.value = False
            self.wait()
            return False

        return True

    def RRC1(self):
        self.object_index = int(self.recv())
        self.word_1 = None
        self.word_2 = None

        if self.noise >= 1 or self.noise > 0 and random.random() < self.noise:
            self.object_index = random.choice([self.object_index - 1 if self.object_index > 0 else self.object_index, self.object_index + 1 if self.object_index < len(self.objects) - 1 else self.object_index])

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

        if self.noise >= 1 or self.noise > 0 and random.random() < self.noise:
            self.object_index = random.choice([self.object_index - 1 if self.object_index > 0 else self.object_index, self.object_index + 1 if self.object_index < len(self.objects) - 1 else self.object_index])

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
