from State import State
from multiprocessing import Value, Process
from ctypes import c_bool
import logging
import sys

class Agent:
    def __init__(self, seed, noise):
        self.seed = seed
        self.noise = noise
        self.running = Value(c_bool, False)
        self.process = Process(target= self.run)
        self.state = State.Start
        self.logger = logging.getLogger("{}.{}".format(self.__class__.__name__, id(self)))
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        self.logger.setLevel(logging.INFO)

    def start(self):
        self.running.value = True
        self.process.start()

    def join(self):
        self.process.join()

    def info(self, msg):
        self.logger.info("{}#{} {}".format(self.__class__.__name__, self.process.pid, msg))

    def debug(self, msg):
        self.logger.debug("{}#{} {}".format(self.__class__.__name__, self.process.pid, msg))

    def send(self, msg):
        self.conn.send(msg)
        self.info("sent: {}".format(msg))

    def wait(self):
        self.barrier.wait()

    def recv(self):
        msg = self.conn.recv()
        self.debug("received: {}".format(msg))
        return msg

    def run(self):
        pass
