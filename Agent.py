from State import State
from multiprocessing import Value, Process, Pipe, Barrier
from ctypes import c_bool
import logging
import sys

class Agent:
    def __init__(self):
        self.running = Value(c_bool, False)
        self.process = Process(target= self.run)
        self.state = State.Start
        self.logger = logging.getLogger("{}.{}".format(self.__class__.__name__, id(self)))
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        self.logger.setLevel(logging.INFO)

    def connect(self, agent):
        self_conn, agent_conn = Pipe()
        self.conn = self_conn
        self.barrier = Barrier(2)
        agent.accept(agent_conn, self.barrier)

    def accept(self, conn, barrier):
        self.conn = conn
        self.barrier = barrier

    def start(self):
        self.running.value = True
        self.process.start()

    def join(self):
        self.process.join()

    def stop(self):
        self.running.value = False
        self.process.join()

    def send(self, msg):
        self.conn.send(msg)
        self.logger.info("{}#{} sent: {}".format(self.__class__.__name__, self.process.pid, msg))

    def wait(self):
        self.barrier.wait()

    def recv(self):
        msg = self.conn.recv()
        self.logger.debug("{}#{} received: {}".format(self.__class__.__name__, self.process.pid, msg))
        return msg

    def run(self):
        pass
