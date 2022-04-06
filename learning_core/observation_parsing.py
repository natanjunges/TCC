from meta_planning.pddl import Action
from meta_planning.observations import State, Observation
from meta_planning.parsers.pddl_parsing import parse_pddl_file
from meta_planning.parsers.parsing_functions import parse_typed_list, parse_state

def parse_observation(observation_file, model):
    observation_pddl = parse_pddl_file("observation", observation_file)
    iterator = iter(observation_pddl)
    tag = next(iterator)
    assert tag == "observation"
    objects_opt = next(iterator)
    assert objects_opt[0] == ":objects"
    object_list = parse_typed_list(objects_opt[1:])
    states = []
    init = next(iterator)
    assert init[0] == ":state"
    new_state = parse_state(init[1:], None, False)
    states.append(new_state)

    for token in iterator:
        if token[0] == ":state":
            new_state = parse_state(token[1:], None, False)
            states.append(new_state)
        elif token[0] == ":action":
            next_action = Action(token[1][0], token[1][1:])

            if new_state.next_action is not None:
                new_state = State([], None)
                states.append(new_state)

            new_state.next_action = next_action

    return Observation(object_list, states, True, True)
