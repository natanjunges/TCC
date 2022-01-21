from Agent import Agent
from time import sleep

class RobotAgent(Agent):
    def run(self):
        while self.running.value:
            self.send("Hello")

            if self.poll():
                print(self.recv())

            sleep(1)
