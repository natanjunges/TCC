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

class Learner:
    objects = [
        TypedObject("object_index_1", "variable"),
        TypedObject("object_index_2", "variable"),
        TypedObject("object_index", "variable"),
        TypedObject("word_1", "variable"),
        TypedObject("word_2", "variable"),
        TypedObject("word", "variable"),
        TypedObject("Integer", "message"),
        TypedObject("String", "message"),
        TypedObject("Boolean", "message"),
        TypedObject("IntegerQuestion", "message"),
        TypedObject("StringQuestion", "message")
    ]
    initial_state = State([
        Literal("set", ["object_index_1"], False),
        Literal("set", ["object_index_2"], False),
        Literal("set", ["object_index"], False),
        Literal("set", ["word_1"], False),
        Literal("set", ["word_2"], False),
        Literal("set", ["word"], False),
        Literal("sent_to_human", ["Integer"], False),
        Literal("sent_to_human", ["String"], False),
        Literal("sent_to_human", ["Boolean"], False),
        Literal("sent_to_human", ["IntegerQuestion"], False),
        Literal("sent_to_human", ["StringQuestion"], False),
        Literal("sent_to_robot", ["Integer"], False),
        Literal("sent_to_robot", ["String"], False),
        Literal("sent_to_robot", ["Boolean"], False),
        Literal("sent_to_robot", ["IntegerQuestion"], False),
        Literal("sent_to_robot", ["StringQuestion"], False)
    ], None)

    def __init__(self, model_file):
        self.builder = ObservationBuilder(self.objects, deepcopy(self.initial_state))
        self.model_file = model_file
        self.model = parse_model(model_file)

    def add_state(self, robot, sent_msg, recv_msg):
        self.builder.add_state(State([
            Literal("set", ["object_index_1"], robot.object_index_1 != None),
            Literal("set", ["object_index_2"], robot.object_index_2 != None),
            Literal("set", ["word"], robot.word != None),
            Literal("sent_to_human", ["Integer"], sent_msg == Message.Integer),
            Literal("sent_to_human", ["String"], sent_msg == Message.String),
            Literal("sent_to_human", ["Boolean"], sent_msg == Message.Boolean),
            Literal("sent_to_human", ["IntegerQuestion"], sent_msg == Message.IntegerQuestion),
            Literal("sent_to_human", ["StringQuestion"], sent_msg == Message.StringQuestion),
            Literal("sent_to_robot", ["Integer"], recv_msg == Message.Integer),
            Literal("sent_to_robot", ["String"], recv_msg == Message.String),
            Literal("sent_to_robot", ["Boolean"], recv_msg == Message.Boolean),
            Literal("sent_to_robot", ["IntegerQuestion"], recv_msg == Message.IntegerQuestion),
            Literal("sent_to_robot", ["StringQuestion"], recv_msg == Message.StringQuestion)
        ], None))

    def add_action(self, state):
        if state == AgentState.TR:
            self.builder.add_action(Action("goto_TR", ["object_index_1", "object_index_2", "word", "Integer"]))
        elif state == AgentState.RRC1:
            self.builder.add_action(Action("goto_RRC1", ["object_index", "word_1", "word_2", "Integer", "IntegerQuestion"]))
        elif state == AgentState.RRC2:
            self.builder.add_action(Action("goto_RRC2", ["object_index_1", "object_index_2", "word", "IntegerQuestion"]))
        elif state == AgentState.CR:
            self.builder.add_action(Action("goto_CR", ["object_index_1", "object_index_2", "Boolean"]))
        elif state == AgentState.TW:
            self.builder.add_action(Action("goto_TW", ["word_1", "word_2", "String"]))
        elif state == AgentState.RWC1:
            self.builder.add_action(Action("goto_RWC1", ["word", "String", "StringQuestion"]))
        elif state == AgentState.RWC2:
            self.builder.add_action(Action("goto_RWC2", ["word_1", "word_2", "StringQuestion"]))
        elif state == AgentState.CW1:
            self.builder.add_action(Action("goto_CW1", ["word_1", "word_2", "Boolean"]))
        elif state == AgentState.CW2:
            self.builder.add_action(Action("goto_CW2", ["object_index_1", "object_index_2", "word"]))
        elif state == AgentState.TIR:
            self.builder.add_action(Action("goto_TIR", ["object_index_1", "object_index_2", "word", "Integer"]))
        elif state == AgentState.RIRC1:
            self.builder.add_action(Action("goto_RIRC1", ["object_index", "word_1", "word_2", "Integer", "IntegerQuestion"]))
        elif state == AgentState.RIRC2:
            self.builder.add_action(Action("goto_RIRC2", ["object_index_1", "object_index_2", "word", "IntegerQuestion"]))
        elif state == AgentState.CIR:
            self.builder.add_action(Action("goto_CIR", ["object_index_1", "object_index_2", "Boolean"]))
        elif state == AgentState.RIC1:
            self.builder.add_action(Action("goto_RIC1", ["word", "String", "StringQuestion"]))
        elif state == AgentState.RIC2:
            self.builder.add_action(Action("goto_RIC2", ["object_index", "word_1", "word_2", "StringQuestion"]))
        elif state == AgentState.CI1:
            self.builder.add_action(Action("goto_CI1", ["object_index", "word_2", "Boolean"]))
        elif state == AgentState.CI2:
            self.builder.add_action(Action("goto_CI2", ["object_index_1", "object_index_2", "word"]))

    def choose(self, current_state, possible_states):
        pass

    def learn(self):
        task = LearningTask(self.model, [self.builder.observation])
        solution = task.learn()
        self.model = solution.learned_model
        self.model.to_file(self.model_file)
