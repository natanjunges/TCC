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

from copy import deepcopy
import os
import os.path

from meta_planning import LearningTask, ModelRecognitionTask
from meta_planning.pddl import TypedObject, Literal, Action
from meta_planning.observations import State
from meta_planning.parsers import parse_model
from meta_planning.parsers.observation_parsing import parse_observation

from .ObservationBuilder import ObservationBuilder
from agent_core.Message import Message
from agent_core.State import State as AgentState

class Learner:
    objects = [
        TypedObject("object-index-1", "oi1"),
        TypedObject("object-index-2", "oi2"),
        TypedObject("object-index", "oi"),
        TypedObject("word-1", "w1"),
        TypedObject("word-2", "w2"),
        TypedObject("word", "w"),
        TypedObject("integer", "i"),
        TypedObject("string", "s"),
        TypedObject("boolean", "b"),
        TypedObject("integer-question", "iq"),
        TypedObject("string-question", "sq")
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
    pre_actions = {
        AgentState.TR: Action("goto-tr-pre", ["object-index-2", "word"]),
        AgentState.RRC1: Action("goto-rrc1-pre", ["word-1", "word-2"]),
        AgentState.RRC2: Action("goto-rrc2-pre", ["word"]),
        AgentState.TW: Action("goto-tw-pre", ["word-2"]),
        AgentState.CW2: Action("goto-cw2-pre", ["object-index-2"]),
        AgentState.TIR: Action("goto-tir-pre", ["object-index-2", "word"]),
        AgentState.RIRC1: Action("goto-rirc1-pre", ["word-1", "word-2"]),
        AgentState.RIRC2: Action("goto-rirc2-pre", ["word"]),
        AgentState.RIC2: Action("goto-ric2-pre", ["word-1"]),
        AgentState.CI2: Action("goto-ci2-pre", ["object-index-2"])
    }
    actions = {
        AgentState.TR: Action("goto-tr", ["object-index-1", "object-index-2",
                                          "word", "integer"]),
        AgentState.RRC1: Action("goto-rrc1", ["object-index", "word-1",
                                              "word-2", "integer",
                                              "integer-question"]),
        AgentState.RRC2: Action("goto-rrc2", ["object-index-1",
                                              "object-index-2", "word",
                                              "integer-question"]),
        AgentState.CR: Action("goto-cr", ["object-index-1", "object-index-2",
                                          "boolean"]),
        AgentState.TW: Action("goto-tw", ["word-1", "word-2", "string"]),
        AgentState.RWC1: Action("goto-rwc1", ["word", "string",
                                              "string-question"]),
        AgentState.RWC2: Action("goto-rwc2", ["word-1", "word-2",
                                              "string-question"]),
        AgentState.CW1: Action("goto-cw1", ["word-1", "word-2", "boolean"]),
        AgentState.CW2: Action("goto-cw2", ["object-index-1", "object-index-2",
                                            "word"]),
        AgentState.TIR: Action("goto-tir", ["object-index-1", "object-index-2",
                                            "word", "integer"]),
        AgentState.RIRC1: Action("goto-rirc1", ["object-index", "word-1",
                                                "word-2", "integer",
                                                "integer-question"]),
        AgentState.RIRC2: Action("goto-rirc2", ["object-index-1",
                                                "object-index-2", "word",
                                                "integer-question"]),
        AgentState.CIR: Action("goto-cir", ["object-index-1", "object-index-2",
                                            "boolean"]),
        AgentState.RIC1: Action("goto-ric1", ["word", "string",
                                              "string-question"]),
        AgentState.RIC2: Action("goto-ric2", ["object-index", "word-1",
                                              "word-2", "string-question"]),
        AgentState.CI1: Action("goto-ci1", ["object-index", "word-2",
                                            "boolean"]),
        AgentState.CI2: Action("goto-ci2", ["object-index-1", "object-index-2",
                                            "word"])
    }
    post_actions = {
        AgentState.CR: Action("goto-cr-post", ["boolean"]),
        AgentState.CW1: Action("goto-cw1-post", ["boolean"]),
        AgentState.CIR: Action("goto-cir-post", ["boolean"]),
        AgentState.CI1: Action("goto-ci1-post", ["boolean"])
    }

    @classmethod
    def apply_arguments(cls, literals, parameters, arguments):
        literals = deepcopy(literals)

        for i in range(len(arguments)):
            arg = arguments[i]
            par = parameters[i].name

            for j in range(len(literals)):
                literals[j] = literals[j].rename_variables({x: arg for x
                                                            in literals[j].args
                                                            if x == par})

        return literals

    def __init__(self, robot):
        self.builder = ObservationBuilder(self.objects, deepcopy(
            self.initial_state))
        self.robot = robot
        self.model = parse_model(self.robot.model_file)
        self.observation_file = "{}/{}/observation.pddl".format(
            self.robot.path_prefix, self.robot.id)
        self.observations = []
        self.parameters_dict = {scheme.name: scheme.parameters for scheme
                                in self.model.schemata}
        self.preconditions_dict = {scheme.name: list(scheme.precondition.parts)
                                   for scheme in self.model.schemata}
        self.effects_dict = {scheme.name: [effect.literal for effect
                                           in scheme.effects]
                             for scheme in self.model.schemata}
        self.inferred_state = set(deepcopy(self.initial_state.literals))

    def reset(self):
        self.builder = ObservationBuilder(self.objects, deepcopy(
            self.initial_state))
        self.model = parse_model(self.robot.model_file)
        self.parameters_dict = {scheme.name: scheme.parameters for scheme
                                in self.model.schemata}
        self.preconditions_dict = {scheme.name: list(scheme.precondition.parts)
                                   for scheme in self.model.schemata}
        self.effects_dict = {scheme.name: [effect.literal for effect
                                           in scheme.effects]
                             for scheme in self.model.schemata}
        self.inferred_state = set(deepcopy(self.initial_state.literals))

        if os.path.isfile(self.observation_file):
            self.observations.append(parse_observation(self.observation_file,
                                                       self.model))
            os.remove(self.observation_file)

    def add_state(self, sent_msg, recv_msg, final=False):
        literals = [
            Literal("set", ["object-index-1"], self.robot.object_index_1
                    is not None),
            Literal("set", ["object-index-2"], self.robot.object_index_2
                    is not None),
            Literal("set", ["word"], self.robot.word is not None),
            Literal("sent-to-human", ["integer"], sent_msg == Message.Integer),
            Literal("sent-to-human", ["string"], sent_msg == Message.String),
            Literal("sent-to-human", ["boolean"], sent_msg == Message.Boolean),
            Literal("sent-to-human", ["integer-question"], sent_msg
                    == Message.IntegerQuestion),
            Literal("sent-to-human", ["string-question"], sent_msg
                    == Message.StringQuestion),
            Literal("sent-to-robot", ["integer"], recv_msg == Message.Integer),
            Literal("sent-to-robot", ["string"], recv_msg == Message.String),
            Literal("sent-to-robot", ["boolean"], recv_msg == Message.Boolean),
            Literal("sent-to-robot", ["integer-question"], recv_msg
                    == Message.IntegerQuestion),
            Literal("sent-to-robot", ["string-question"], recv_msg
                    == Message.StringQuestion)
        ]

        if final:
            literals += [
                Literal("set", ["object-index"], False),
                Literal("set", ["word-1"], False),
                Literal("set", ["word-2"], False)
            ]

        self.builder.add_state(State(literals, None))

    def add_action(self, state):
        if state in self.pre_actions and not self.can_apply_action(
                self.inferred_state, self.actions[state]):
            self.builder.add_action(deepcopy(self.pre_actions[state]))
            self.inferred_state = self.apply_action(self.inferred_state,
                                                    self.pre_actions[state])

        self.builder.add_action(deepcopy(self.actions[state]))
        self.inferred_state = self.apply_action(self.inferred_state,
                                                self.actions[state])

    def add_post_action(self, state):
        self.builder.add_action(deepcopy(self.post_actions[state]))
        self.inferred_state = self.apply_action(self.inferred_state,
                                                self.post_actions[state])

    def choose(self, possible_states=None):
        a = 2
        g = 2
        next_states = [AgentState.TR, AgentState.RRC1, AgentState.RRC2,
                       AgentState.CR, AgentState.TW, AgentState.RWC1,
                       AgentState.RWC2, AgentState.CW1, AgentState.CW2]

        if self.robot.interaction == AgentState.SecondInteraction:
            next_states += [AgentState.TIR, AgentState.RIRC1, AgentState.RIRC2,
                            AgentState.CIR, AgentState.RIC1, AgentState.RIC2,
                            AgentState.CI1, AgentState.CI2]

        if possible_states is None:
            possible_states = next_states

        states = deepcopy(possible_states)
        weights = []
        sum = 0
        i = 0

        while i < len(states):
            stack = [[states[i]]]
            subweights = [[0, 0]]
            state_trajectory = [self.inferred_state]

            while len(stack) > 0:
                state = stack[-1].pop()
                cba = self.can_apply_action(state_trajectory[-1],
                                            self.actions[state])

                if (not cba and state in self.pre_actions
                        and self.can_apply_action(state_trajectory[-1],
                                                  self.pre_actions[state])):
                    inferred_substate = self.apply_action(
                        state_trajectory[-1], self.pre_actions[state])
                    cba = self.can_apply_action(inferred_substate,
                                                self.actions[state])
                    inferred_substate = self.apply_action(inferred_substate,
                                                          self.actions[state])
                else:
                    inferred_substate = self.apply_action(state_trajectory[-1],
                                                          self.actions[state])

                if state in self.post_actions and self.can_apply_action(
                        inferred_substate, self.post_actions[state]):
                    inferred_substate = self.apply_action(
                        inferred_substate, self.post_actions[state])

                if inferred_substate in state_trajectory:
                    pass
                elif state in {AgentState.CW2, AgentState.CI2}:
                    subweights[-1][0] += (a if cba else 1) * g
                    subweights[-1][1] += 1
                elif not cba:
                    subweights[-1][0] += 1
                    subweights[-1][1] += 1
                else:
                    if state == AgentState.RRC2:
                        stack.append([AgentState.TR, AgentState.CR])
                    elif state in {AgentState.RWC2, AgentState.RIC2}:
                        if (self.robot.interaction
                                == AgentState.FirstInteraction):
                            stack.append([AgentState.TW, AgentState.CW1])
                        elif (self.robot.interaction
                              == AgentState.SecondInteraction):
                            stack.append([AgentState.TW, AgentState.CW1,
                                          AgentState.CI1])
                    elif state == AgentState.RIRC2:
                        stack.append([AgentState.TIR, AgentState.CIR])
                    else:
                        stack.append(deepcopy(next_states))

                    subweights.append([0, 0])
                    state_trajectory.append(inferred_substate)
                    continue

                while len(stack) > 0 and len(stack[-1]) == 0:
                    stack.pop()
                    subweight = subweights.pop()

                    if subweight[1] > 0:
                        avg = subweight[0] / subweight[1] * a

                        if len(subweights) > 0:
                            subweights[-1][0] += avg
                            subweights[-1][1] += 1
                        else:
                            subweights.append(avg)

                    state_trajectory.pop()

            if len(subweights) > 0:
                weights.append(subweights[0])
                sum += subweights[0]
                i += 1
            else:
                states.pop(i)

        for i in range(len(possible_states)):
            if i >= len(states) or states[i] != possible_states[i]:
                states.insert(i, possible_states[i])
                weights.insert(i, 1)
                sum += 1

        weights = [weight / sum for weight in weights]
        return self.robot.random.choices(states, weights)[0]

    def apply_action(self, state, action):
        effects = self.apply_arguments(self.effects_dict[action.name],
                                       self.parameters_dict[action.name],
                                       action.arguments)
        state = state.difference({effect.flip() for effect in effects})
        state = state.union(effects)
        return state

    def can_apply_action(self, state, action):
        preconditions = self.apply_arguments(
            self.preconditions_dict[action.name],
            self.parameters_dict[action.name], action.arguments)
        return state.issuperset(preconditions)

    def learn(self):
        with open(self.observation_file, "w") as file:
            file.write(str(self.builder.observation))

        self.observations.append(self.builder.observation)
        task = LearningTask(self.model, self.observations,
                            allow_deletions=True)
        solution = task.learn(suffix=str(self.robot.id))

        if solution.solution_found:
            solution.learned_model.to_file(self.robot.model_file)
