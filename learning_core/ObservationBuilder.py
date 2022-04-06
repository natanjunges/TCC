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

from meta_planning.observations import State, Observation

class ObservationBuilder:
    def __init__(self, objects, initial_state):
        initial_state.next_action = None
        self.observation = Observation(objects, [initial_state], True, True)

    def add_state(self, state):
        state.next_action = None
        self.observation.all_actions_observed = self.observation.all_actions_observed and self.observation.states[-1].next_action is not None
        self.observation.states.append(state)
        self.observation.bounded = self.observation.all_states_observed or self.observation.all_actions_observed
        self.observation.length += 1
        self.observation.number_of_states += 1

    def add_action(self, action):
        if self.observation.states[-1].next_action is None:
            self.observation.states[-1].next_action = action
        else:
            self.observation.all_states_observed = False
            self.observation.states.append(State([], action))
            self.observation.bounded = self.observation.all_actions_observed
            self.observation.length += 1

        self.observation.number_of_actions += 1
