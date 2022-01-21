from Agent import Agent
from time import sleep

class HumanAgent(Agent):
    def run(self):
        while self.running.value:
            self.send("Hi")

            if self.poll():
                print(self.recv())

            sleep(1)
