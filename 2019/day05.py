import intcode

# Initialize: open file, turn all op codes into integers
with open('day05.txt') as f:
    # split line into operation list
    opsAsStrings = f.read().split(",")
    # turn them all into integers
    ops = list(map(int, opsAsStrings))

myOps = ops.copy()
print ("Part One: %s" % intcode.run(myOps, [1]))

myOps = ops.copy()
print ("Part Two: %s" % intcode.run(myOps, [5]))
