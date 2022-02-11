from multiprocessing import Value, Process, Pipe
from ctypes import c_bool

class Agent:
    def __init__(self, objects):
        self.objects = objects
        self.running = Value(c_bool, False)
        self.process = Process(target= self.run)

    def connect(self, agent):
        self_conn, agent_conn = Pipe()
        self.conn = self_conn
        agent.accept(agent_conn)

    def accept(self, conn):
        self.conn = conn

    def start(self):
        self.running.value = True
        self.process.start()

    def stop(self):
        self.running.value = False
        self.process.join()

    def send(self, msg):
        self.conn.send(msg)

    def poll(self):
        return self.conn.poll()

    def wait(self):
        self.conn.poll(None)

    def recv(self):
        return self.conn.recv()

    def run(self):
        pass
