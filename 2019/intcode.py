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
    def __init__(self, ops, output = None, address = 0, memory = {}, rel_base = 0, done = False):
        self.ops = ops # the instruction set
        self.output = output # any previous output
        self.address = address # index of next instruction to execute
        self.memory = memory # the memory heap
        self.rel_base = rel_base # the relative base from which to calculate relative addresses
        self.done = done # flag to indicate whether this program has hit opcode 99
    def __repr__(self):
        return "Last Output: {}, Rel Base: {}. Op Address: {}".format(self.output, self.rel_base, self.address)

def run(state, inp):
    return _run(state.ops, inp, state.address, state.output, state.memory, state.rel_base)

def _run(ops, input, starting_addr, last_output, memory, rel_base):
    # start at the front of the inputs
    input_idx = 0
    # no output yet
    output = last_output
    # assign to i for brevity
    i = starting_addr
    while ops[i] != 99:
        instruction = Instruction(ops[i])
        if instruction.operation is Operation.ADDITION:
            first = _get_resolved_arg(instruction, ops, memory, rel_base, i, 1)
            second = _get_resolved_arg(instruction, ops, memory, rel_base, i, 2)
            destination = _get_resolved_position(instruction, ops, rel_base, i, 3)
            _write(first + second, destination, ops, memory)
            i += 4
        elif instruction.operation is Operation.MULTIPLICATION:
            first = _get_resolved_arg(instruction, ops, memory, rel_base, i, 1)
            second = _get_resolved_arg(instruction, ops, memory, rel_base, i, 2)
            destination = _get_resolved_position(instruction, ops, rel_base, i, 3)
            _write(first * second, destination, ops, memory)
            i += 4
        elif instruction.operation is Operation.INPUT:
            destination = _get_resolved_position(instruction, ops, rel_base, i, 1)
            _write(int(input[input_idx]), destination, ops, memory)
            input_idx += 1
            i += 2
        elif instruction.operation is Operation.OUTPUT:
            output = _get_resolved_arg(instruction, ops, memory, rel_base, i, 1)
            i += 2
            return ProgramState(ops, output, i, memory, rel_base, False)
        elif instruction.operation is Operation.JUMP_IF_TRUE:
            first = _get_resolved_arg(instruction, ops, memory, rel_base, i, 1)
            second = _get_resolved_arg(instruction, ops, memory, rel_base, i, 2)
            if first != 0:
                i = second
            else:
                i += 3
        elif instruction.operation is Operation.JUMP_IF_FALSE:
            first = _get_resolved_arg(instruction, ops, memory, rel_base, i, 1)
            second = _get_resolved_arg(instruction, ops, memory, rel_base, i, 2)
            if first == 0:
                i = second
            else:
                i += 3
        elif instruction.operation is Operation.LESS_THAN:
            first = _get_resolved_arg(instruction, ops, memory, rel_base, i, 1)
            second = _get_resolved_arg(instruction, ops, memory, rel_base, i, 2)
            destination = _get_resolved_position(instruction, ops, rel_base, i, 3)
            _write(1 if first < second else 0, destination, ops, memory)
            i += 4
        elif instruction.operation is Operation.EQUALS:
            first = _get_resolved_arg(instruction, ops, memory, rel_base, i, 1)
            second = _get_resolved_arg(instruction, ops, memory, rel_base, i, 2)
            destination = _get_resolved_position(instruction, ops, rel_base, i, 3)
            _write(1 if first == second else 0, destination, ops, memory)
            i += 4
        elif instruction.operation is Operation.RELATIVE_BASE:
            rel_offset = _get_resolved_arg(instruction, ops, memory, rel_base, i, 1)
            rel_base += rel_offset
            i += 2
    return ProgramState(ops, output, i, {}, rel_base, True)

# Returns the number at the given position (0 being the rightmost)
def _get_nth_digit(n, number):
    return number // 10**n % 10

def _get_resolved_arg(instruction, ops, memory, rel_base, address, arg):
    # ops[i+1] if instruction.modes[0] is Mode.IMMEDIATE else ops[ops[i+1]]
    mode = instruction.modes[arg-1]
    if mode is Mode.IMMEDIATE:
        return ops[address+arg]
    
    final_addr = ops[address+arg] # Here, mode is POSITION or RELATIVE
    # if RELATIVE add the relative base
    if mode is Mode.RELATIVE:
        final_addr += rel_base
    return ops[final_addr] if final_addr < len(ops) else memory.get(final_addr,0)

def _get_resolved_position(instruction, ops, rel_base, address, arg):
    # ops[i+1] if instruction.modes[0] is Mode.IMMEDIATE else ops[ops[i+1]]
    mode = instruction.modes[arg-1]
    if mode is Mode.POSITION:
        return ops[address+arg]
    elif mode is Mode.RELATIVE:
        return ops[address+arg]+rel_base
    else:
        print ("Bonkers! Unhandled case")

def _write(value, destination, ops, memory):
    if destination < len(ops):        
        ops[destination] = value
    else:
        memory[destination] = value

