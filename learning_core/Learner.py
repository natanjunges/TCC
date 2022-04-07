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
#
# Additional permission under GNU GPL version 3 section 7
#
# If you modify TCC, or any covered work, by linking or combining it with
# meta-planning, numpy or Madagascar (or modified versions of those
# libraries/programs), containing parts covered by the terms of
# meta-planning's (detailed in README.md), numpy's (BSD 3-Clause License)
# or Madagascar's (detailed in README.md) licenses, the licensors of TCC
# grant you additional permission to convey the resulting work.

from .ObservationBuilder import ObservationBuilder
from agent_core.Message import Message
from agent_core.State import State as AgentState
from meta_planning import LearningTask
from meta_planning.pddl import TypedObject, Literal, Action
from meta_planning.observations import State
from meta_planning.parsers import parse_model
from copy import deepcopy
import os
import os.path

class Learner:
    objects = [
        TypedObject("object-index-1", "variable"),
        TypedObject("object-index-2", "variable"),
        TypedObject("object-index", "variable"),
        TypedObject("word-1", "variable"),
        TypedObject("word-2", "variable"),
        TypedObject("word", "variable"),
        TypedObject("integer", "message"),
        TypedObject("string", "message"),
        TypedObject("boolean", "message"),
        TypedObject("integer-question", "message"),
        TypedObject("string-question", "message")
    ]
    initial_state = State([
        Literal("set", ["object-index-1"], False),
        Literal("set", ["object-index-2"], False),
        Literal("set", ["object-index"], False),
        Literal("set", ["word-1"], False),
        Literal("set", ["word-2"], False),
        Literal("set", ["word"], False),
        Literal("sent-to-human", ["integer"], False),
        Literal("sent-to-human", ["string"], False),
        Literal("sent-to-human", ["boolean"], False),
        Literal("sent-to-human", ["integer-question"], False),
        Literal("sent-to-human", ["string-question"], False),
        Literal("sent-to-robot", ["integer"], False),
        Literal("sent-to-robot", ["string"], False),
        Literal("sent-to-robot", ["boolean"], False),
        Literal("sent-to-robot", ["integer-question"], False),
        Literal("sent-to-robot", ["string-question"], False)
    ], None)

    def __init__(self, robot):
        self.builder = ObservationBuilder(self.objects, deepcopy(self.initial_state))
        self.robot = robot
        self.model = parse_model(self.robot.model_file)

    def reset(self):
        self.builder = ObservationBuilder(self.objects, deepcopy(self.initial_state))
        self.model = parse_model(self.robot.model_file)

    def add_state(self, sent_msg, recv_msg):
        self.builder.add_state(State([
            Literal("set", ["object-index-1"], self.robot.object_index_1 is not None),
            Literal("set", ["object-index-2"], self.robot.object_index_2 is not None),
            Literal("set", ["word"], self.robot.word is not None),
            Literal("sent-to-human", ["integer"], sent_msg == Message.Integer),
            Literal("sent-to-human", ["string"], sent_msg == Message.String),
            Literal("sent-to-human", ["boolean"], sent_msg == Message.Boolean),
            Literal("sent-to-human", ["integer-question"], sent_msg == Message.IntegerQuestion),
            Literal("sent-to-human", ["string-question"], sent_msg == Message.StringQuestion),
            Literal("sent-to-robot", ["integer"], recv_msg == Message.Integer),
            Literal("sent-to-robot", ["string"], recv_msg == Message.String),
            Literal("sent-to-robot", ["boolean"], recv_msg == Message.Boolean),
            Literal("sent-to-robot", ["integer-question"], recv_msg == Message.IntegerQuestion),
            Literal("sent-to-robot", ["string-question"], recv_msg == Message.StringQuestion)
        ], None))

    def add_action(self, state):
        if state == AgentState.TR:
            self.builder.add_action(Action("goto-tr", ["object-index-1", "object-index-2", "word", "integer"]))
        elif state == AgentState.RRC1:
            self.builder.add_action(Action("goto-rrc1", ["object-index", "word-1", "word-2", "integer", "integer-question"]))
        elif state == AgentState.RRC2:
            self.builder.add_action(Action("goto-rrc2", ["object-index-1", "object-index-2", "word", "integer-question"]))
        elif state == AgentState.CR:
            self.builder.add_action(Action("goto-cr", ["object-index-1", "object-index-2", "boolean"]))
        elif state == AgentState.TW:
            self.builder.add_action(Action("goto-tw", ["word-1", "word-2", "string"]))
        elif state == AgentState.RWC1:
            self.builder.add_action(Action("goto-rwc1", ["word", "string", "string-question"]))
        elif state == AgentState.RWC2:
            self.builder.add_action(Action("goto-rwc2", ["word-1", "word-2", "string-question"]))
        elif state == AgentState.CW1:
            self.builder.add_action(Action("goto-cw1", ["word-1", "word-2", "boolean"]))
        elif state == AgentState.CW2:
            self.builder.add_action(Action("goto-cw2", ["object-index-1", "object-index-2", "word"]))
        elif state == AgentState.TIR:
            self.builder.add_action(Action("goto-tir", ["object-index-1", "object-index-2", "word", "integer"]))
        elif state == AgentState.RIRC1:
            self.builder.add_action(Action("goto-rirc1", ["object-index", "word-1", "word-2", "integer", "integer-question"]))
        elif state == AgentState.RIRC2:
            self.builder.add_action(Action("goto-rirc2", ["object-index-1", "object-index-2", "word", "integer-question"]))
        elif state == AgentState.CIR:
            self.builder.add_action(Action("goto-cir", ["object-index-1", "object-index-2", "boolean"]))
        elif state == AgentState.RIC1:
            self.builder.add_action(Action("goto-ric1", ["word", "string", "string-question"]))
        elif state == AgentState.RIC2:
            self.builder.add_action(Action("goto-ric2", ["object-index", "word-1", "word-2", "string-question"]))
        elif state == AgentState.CI1:
            self.builder.add_action(Action("goto-ci1", ["object-index", "word-2", "boolean"]))
        elif state == AgentState.CI2:
            self.builder.add_action(Action("goto-ci2", ["object-index-1", "object-index-2", "word"]))

    def choose(self, possible_states):
        return possible_states

    def learn(self):
        task = LearningTask(self.model, [self.builder.observation])
        solution = task.learn()

        if solution.solution_found:
            solution.learned_model.to_file(self.robot.model_file)
