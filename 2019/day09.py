from intcode import ProgramState
from intcode import run


with open('day09.txt') as f:
    # split line into operation list
    opsAsStrings = f.read().split(",")
    # turn them all into integers
    ops = list(map(int, opsAsStrings))

def boost(ops, inp):
    outputs = []
    state = run(ProgramState(ops), [inp])
    while not state.done:
        print (state.output)
        outputs.append(state.output)
        state = run(state, [])
    print (state.memory)
    return outputs

# Part One
print ("Part One: %s" % boost(ops, 1))
print ("Part Two: %s" % boost(ops, 2))
