import intcode

# Initialize: open file, turn all op codes into integers
with open('day05.txt') as f:
    # split line into operation list
    opsAsStrings = f.read().split(",")
    # turn them all into integers
    ops = list(map(int, opsAsStrings))

myOps = ops.copy()

latestOutput = None
state = intcode.run(myOps, [1])
while not state.done:
    latestOutput = state.output
    # print (latestOutput)
    state = intcode.run(myOps, [], state.address)
print ("Part One: %s" % latestOutput)

myOps = ops.copy()
print ("Part Two: %s" % intcode.run(myOps, [5]).output)
