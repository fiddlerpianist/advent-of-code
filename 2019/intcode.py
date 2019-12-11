from enum import Enum

class Operation(Enum):
    ADDITION = 1
    MULTIPLICATION = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    RELATIVE_BASE = 9
    TERMINATION = 99

class Mode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2

class Instruction:
    def __init__(self, opcode):
        # instruction: 1 is add, 2 is multiply, 3 is input, 4 is output, 99 is end
        self.operation = Operation(_get_nth_digit(1, opcode) * 10 + _get_nth_digit(0, opcode))
        # mode: 0 is indirect, 1 is immediate
        self.modes = list(map(Mode, [_get_nth_digit(2, opcode), _get_nth_digit(3, opcode), _get_nth_digit(4, opcode)]))
        
    def __str__(self):
        return "{}, {}".format(repr(self.operation), self.modes)

class ProgramState:
    def __init__(self, ops, output = None, address = 0, memory = {}, done = False):
        self.output = output
        self.ops = ops
        self.address = address
        self.memory = memory
        self.done = done

def run(state, inp):
    return _run(state.ops, inp, state.address, state.output, state.memory)

def _run(ops, input, startingAddress, lastOutput, memory):
    # start at the front of the inputs
    inputIndex = 0
    # relative base starts at 0
    relativeBase = 0
    # no output yet
    output = lastOutput
    # assign to i for brevity
    i = startingAddress
    while ops[i] != 99:
        instruction = Instruction(ops[i])
        if instruction.operation is Operation.ADDITION:
            first = ops[i+1] if instruction.modes[0] is Mode.IMMEDIATE else ops[ops[i+1]]
            second = ops[i+2] if instruction.modes[1] is Mode.IMMEDIATE else ops[ops[i+2]]
            result = first + second
            # the last mode should *always* be POSITION
            ops[ops[i+3]] = result
            i += 4
        elif instruction.operation is Operation.MULTIPLICATION:
            first = ops[i+1] if instruction.modes[0] is Mode.IMMEDIATE else ops[ops[i+1]]
            second = ops[i+2] if instruction.modes[1] is Mode.IMMEDIATE else ops[ops[i+2]]
            val = first * second
            # the last mode should *always* be POSITION
            ops[ops[i+3]] = val
            i += 4
        elif instruction.operation is Operation.INPUT:
            ops[ops[i+1]] = int(input[inputIndex])
            inputIndex += 1
            i += 2
        elif instruction.operation is Operation.OUTPUT:
            output = ops[ops[i+1]]
            i += 2
            return ProgramState(ops, output, i)
        elif instruction.operation is Operation.JUMP_IF_TRUE:
            first = ops[i+1] if instruction.modes[0] is Mode.IMMEDIATE else ops[ops[i+1]]
            second = ops[i+2] if instruction.modes[1] is Mode.IMMEDIATE else ops[ops[i+2]]
            if first != 0:
                i = second
            else:
                i += 3
        elif instruction.operation is Operation.JUMP_IF_FALSE:
            first = ops[i+1] if instruction.modes[0] is Mode.IMMEDIATE else ops[ops[i+1]]
            second = ops[i+2] if instruction.modes[1] is Mode.IMMEDIATE else ops[ops[i+2]]
            if first == 0:
                i = second
            else:
                i += 3
        elif instruction.operation is Operation.LESS_THAN:
            first = ops[i+1] if instruction.modes[0] is Mode.IMMEDIATE else ops[ops[i+1]]
            second = ops[i+2] if instruction.modes[1] is Mode.IMMEDIATE else ops[ops[i+2]]
            ops[ops[i+3]] = 1 if first < second else 0
            i += 4
        elif instruction.operation is Operation.EQUALS:
            first = ops[i+1] if instruction.modes[0] is Mode.IMMEDIATE else ops[ops[i+1]]
            second = ops[i+2] if instruction.modes[1] is Mode.IMMEDIATE else ops[ops[i+2]]
            ops[ops[i+3]] = 1 if first == second else 0
            i += 4
        elif instruction.operation is Operation.RELATIVE_BASE:
            if instruction.modes[0] is Mode.IMMEDIATE:
                relativeBase += ops[i+1]
            elif instruction.modes[0] is Mode.POSITION:
                relativeBase += ops[ops[i+1]]
            else: # Relative mode
                #relativeBase += 
                pass
            #relativeBase += ops[i+1] if  else ops[ops[i+1]]
            #i += 2
    return ProgramState(ops, output, i, {}, True)

# Returns the number at the given position (0 being the rightmost)
def _get_nth_digit(n, number):
    return number // 10**n % 10
