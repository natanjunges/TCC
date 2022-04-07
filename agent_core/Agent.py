# This file is part of TCC
# Copyright (C) 2022  Natan Junges <natanjunges@alunos.utfpr.edu.br>
#
# TCC is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# TCC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TCC.  If not, see <https://www.gnu.org/licenses/>.

from .State import State
from multiprocessing import Process
import logging
import sys
import random

class Agent:
    SIMULATION= 25
    SENT_MESSAGES= 20
    RECEIVED_MESSAGES= 18
    STATES= 12
    SYNCHRONIZATION= 10

    def __init__(self, id, path_prefix, seed, noise, interaction):
        self.id = id
        self.path_prefix = path_prefix
        self.seed = seed
        self.noise = noise
        self.interaction = interaction
        self.process = Process(target= self.run)
        self.state = State.Start
        self.logger = logging.getLogger("{}.{}".format(self.__class__.__name__, self.id))
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        self.logger.setLevel(self.SENT_MESSAGES)

    def start(self):
        self.process.start()

    def join(self):
        self.process.join()

    def reset(self, seed= None, noise= None, interaction= None):
        if seed is not None:
            self.seed = seed

        if noise is not None:
            self.noise = noise

        if interaction is not None:
            self.interaction = interaction

        self.process = Process(target= self.run)

    def log(self, level, msg):
        self.logger.log(level, "{}#{} {}".format(self.__class__.__name__, self.id, msg))

    def send(self, msg):
        self.conn.send(msg)
        self.log(self.SENT_MESSAGES, "sent: " + msg)

    def recv(self):
        msg = self.conn.recv()
        self.log(self.RECEIVED_MESSAGES, "received: " + msg)
        return msg

    def wait(self):
        self.log(self.SYNCHRONIZATION, "waiting")
        self.barrier.wait()
        self.log(self.SYNCHRONIZATION, "continuing")

    def notify(self):
        self.log(self.SYNCHRONIZATION, "notifying")
        self.barrier.wait()
        self.log(self.SYNCHRONIZATION, "notified")

    def run(self):
        random.seed(self.seed)
        self.object_index_1 = None
        self.object_index_2 = None
        self.word = None
