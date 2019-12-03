 
def opcode_run(ops):
    i = 0
    while ops[i] != 99:
        if ops[i] == 1:
            val = ops[ops[i+1]] + ops[ops[i+2]]
            ops[ops[i+3]] = val
        elif ops[i] == 2:
            val = ops[ops[i+1]] * ops[ops[i+2]]
            ops[ops[i+3]] = val
        else:
            break
        i += 4
    return ops[0]

# Initialize: open file, turn all op codes into integers
with open('day02.txt') as f:
    # split line into operation list
    opsAsStrings = f.read().split(",")
    # turn them all into integers
    ops = list(map(int, opsAsStrings))

# Part One: Find the value at position 0 after the program halts when position 1 is 12 and position 2 is 2
myOps = ops.copy()
myOps[1] = 12
myOps[2] = 2
print ("Part One: %i" % opcode_run(myOps))

# Part Two: Find the input noun and verb that cause the program to produce the output 19690720. What is 100 * noun + verb?
for i in range(0,98):
    for j in range(0,98):
        myOps = ops.copy()
        myOps[1] = i
        myOps[2] = j
        result = opcode_run(myOps)
        if result == 19690720:
            print ("Part Two: noun is %i, verb is %i. Answer is %i" % (i,j,100*i+j))

