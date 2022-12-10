from util import run_day


ADDX_OPCODE = "addx"
NOPE_OPCODE = "noop"


def parse_instruction(line: str):
    match line.split(" "):
        case [addx, number]:
            return (ADDX_OPCODE, int(number))
        case ["noop"]:
            return (NOPE_OPCODE,)


VAL_KEY = "value"
CYCLE_KEY = "cycles"


def make_cpu():
    cpu = {}
    cpu[VAL_KEY] = 1
    cpu[CYCLE_KEY] = 0
    return cpu


def run_trace(cpu, trace):
    curr_cycle = cpu[CYCLE_KEY]
    if (curr_cycle - 20) % 40 == 0:
        trace[curr_cycle] = cpu[VAL_KEY]


def invoke(cpu, instruciton, trace):
    match instruciton:
        case (ADDX_OPCODE, arg):
            cpu[CYCLE_KEY] += 1
            run_trace(cpu, trace)
            cpu[CYCLE_KEY] += 1
            run_trace(cpu, trace)
            cpu[VAL_KEY] += arg
        case (NOPE_OPCODE):
            cpu[CYCLE_KEY] += 1
            run_trace(cpu, trace)


def part1(input):
    with open(input) as f:
        cpu = make_cpu()
        tracer = {}
        for i in f:
            instruction = parse_instruction(i.strip())
            print(instruction)
            print(cpu)
            invoke(cpu, instruction, tracer)
            print(cpu)
            print(tracer)
            print("-" * 20)
        sum = 0 
        for (k,v) in tracer.items():
            if k > 220:
                break
            sum += k*v
        return sum


def part2(input):
    pass


run_day(10, part1, part2)
#part1('input/day10-sample.txt')
