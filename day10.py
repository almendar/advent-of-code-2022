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
        case(ADDX_OPCODE, arg):
            cpu[CYCLE_KEY] += 1
            run_trace(cpu, trace)
            cpu[CYCLE_KEY] += 1
            run_trace(cpu, trace)
            cpu[VAL_KEY] += arg
        case(NOPE_OPCODE):
            cpu[CYCLE_KEY] += 1
            run_trace(cpu, trace)


def part1(input):
    with open(input) as f:
        cpu = make_cpu()
        tracer = {}
        for i in f:
            instruction = parse_instruction(i.strip())
            invoke(cpu, instruction, tracer)
        sum = 0
        for (k, v) in tracer.items():
            if k > 220:
                break
            sum += k * v
        return sum


def print_pixel(cycle, sprite_pos):
    if cycle in range(sprite_pos - 1, sprite_pos + 2):
        print("#", end="")
    else:
        print(".", end="")


def part2(input):
    cpu = make_cpu()
    busy_proc = False
    increment = -1
    sprite_pos = 1
    with open(input) as f:
        for cycle in range(1, 241):
            screen_print = (cycle - 1) % 40
            if not busy_proc:
                instruction = f.readline().strip()
                match parse_instruction(instruction):
                    case(ADDX_OPCODE, number):
                        busy_proc = True
                        increment = number
                    case(NOPE_OPCODE,):
                        pass
                print_pixel(screen_print, sprite_pos)
            else:
                print_pixel(screen_print, sprite_pos)
                busy_proc = False
                cpu[VAL_KEY] += increment
                sprite_pos = cpu[VAL_KEY]
            if cycle % 40 == 0:
                print()


print(part1("input/day10-sample.txt"))
print(part1("input/day10-input.txt"))
print()
part2("input/day10-sample.txt")
print()
part2("input/day10-input.txt")
