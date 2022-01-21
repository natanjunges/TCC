from multiprocessing import Value, Process
from ctypes import c_bool

class Agent:
    def __init__(self, conn):
        self.conn = conn
        self.running = Value(c_bool, False)
        self.process = Process(target= self.run)

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

    def recv(self):
        return self.conn.recv()

    def run(self):
        while self.running.value:
            pass
