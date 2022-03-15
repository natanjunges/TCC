from State import State
from multiprocessing import Process
import logging
import sys

class Agent:
    def __init__(self, seed, noise, interaction):
        self.seed = seed
        self.noise = noise
        self.interaction = interaction
        self.process = Process(target= self.run)
        self.state = State.Start
        self.logger = logging.getLogger("{}.{}".format(self.__class__.__name__, id(self)))
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        self.logger.setLevel(logging.INFO)

    def start(self):
        self.process.start()

    def join(self):
        self.process.join()

    def reset(self, seed= None, noise= None, interaction= None):
        if seed != None:
            self.seed = seed

        if noise != None:
            self.noise = noise

        if interaction != None:
            self.interaction = interaction

        self.process = Process(target= self.run)

    def info(self, msg):
        self.logger.info("{}#{} {}".format(self.__class__.__name__, self.process.pid, msg))

    def debug(self, msg):
        self.logger.debug("{}#{} {}".format(self.__class__.__name__, self.process.pid, msg))

    def send(self, msg):
        self.conn.send(msg)
        self.info("sent: {}".format(msg))

    def recv(self):
        msg = self.conn.recv()
        self.debug("received: {}".format(msg))
        return msg

    def wait(self):
        self.barrier.wait()

    def run(self):
        pass
