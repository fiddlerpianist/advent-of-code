from itertools import permutations
from intcode import ProgramState
from intcode import run

def part_one(ops):
    thrusterSignals = []
    for phaseCombo in list(permutations(range(0, 5))):
        # do this for 5 amplifiers
        output = 0
        for i in range(0,5):
            # run the program using a copy of the instructions using the next phase in the combo and feed the output to the next iteration
            #output = intcode.run(ops.copy(), [phaseCombo[i], output])
            output = get_final_output(ops.copy(), [phaseCombo[i], output])
        thrusterSignals.append(output)
    return max(thrusterSignals)

def get_final_output(ops, input):
    latestOutput = None
    state = run(ProgramState(ops), input)
    while not state.done:
        latestOutput = state.output
        # print (latestOutput)
        state = run(ProgramState(ops, None, state.address), [])
    return latestOutput

with open('day07.txt') as f:
    # split line into operation list
    opsAsStrings = f.read().split(",")
    # turn them all into integers
    ops = list(map(int, opsAsStrings))

# Part One
print ("Part One: %i" % part_one(ops))


def part_two(ops):
    thrusterSignals = []
    for phaseCombo in list(permutations(range(5, 10))):
        # output starts at 0 and is initisl input
        output = 0
        states = []
        for i in range(0,5):
            # run the program using a copy of the instructions using the next phase in the combo,
            # saving the state and feed the output to the next iteration
            state = run(ProgramState(ops.copy()), [phaseCombo[i], output])
            output = state.output
            states.append(state)
        while states[4].done is False:
            for i in range(0,5):
                state = run(ProgramState(states[i].ops, states[i].output, states[i].address), [output])
                output = state.output
                # assign new state to this amplifier
                states[i] = state
        thrusterSignals.append(output)
    return max(thrusterSignals)

print ("Part Two: %i" % part_two(ops))