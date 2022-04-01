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
        self.logger.info("{}#{} {}".format(self.__class__.__name__, self.id, msg))

    def debug(self, msg):
        self.logger.debug("{}#{} {}".format(self.__class__.__name__, self.id, msg))

    def send(self, msg):
        self.conn.send(msg)
        self.info("sent: " + msg)

    def recv(self):
        msg = self.conn.recv()
        self.debug("received: " + msg)
        return msg

    def wait(self):
        self.debug("waiting")
        self.barrier.wait()
        self.debug("continuing")

    def notify(self):
        self.debug("notifying")
        self.barrier.wait()
        self.debug("notified")

    def run(self):
        random.seed(self.seed)
        self.info("seed: {}".format(self.seed))
        self.info("noise: {}".format(self.noise))
        self.info("interaction: " + ("FirstInteraction" if self.interaction == State.FirstInteraction else "SecondInteraction"))
        self.object_index_1 = None
        self.object_index_2 = None
        self.word = None
