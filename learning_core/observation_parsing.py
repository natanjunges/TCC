from meta_planning.pddl import Literal, Action
from meta_planning.observations import State, Observation

from meta_planning.parsers.pddl_parsing import parse_pddl_file
from meta_planning.parsers.parsing_functions import parse_typed_list, parse_state

from meta_planning.functions import generate_all_literals

import random
import itertools







def parse_observation(observation_file, model):

    predicates = model.predicates
    types = model.types

    observation_pddl = parse_pddl_file('observation', observation_file)

    random.seed(123)

    iterator = iter(observation_pddl)

    tag = next(iterator)
    assert tag == "observation"

    objects_opt = next(iterator)
    assert objects_opt[0] == ":objects"
    object_list = parse_typed_list(objects_opt[1:])

    all_literals = set(generate_all_literals(predicates, object_list, types))


    states = []


    init = next(iterator)
    assert init[0] == ":state"
    new_state = parse_state(init[1:], all_literals)
    states.append(new_state)


    for token in iterator:
        if token[0] == ':state':
            new_state = parse_state(token[1:], all_literals)
            states.append(new_state)
        elif token[0] == ':action':
            next_action = Action(token[1][0], token[1][1:])

            if new_state.next_action is not None:
                new_state = State([], None)
                states.append(new_state)

            new_state.next_action = next_action




    return Observation(object_list, states, True, True)
