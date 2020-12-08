#!/env/python3

import re

text_file = open("Day_08/input", "r")
lines = [x.strip() for x in text_file.readlines()]

pattern = re.compile(r'^(?P<inst>\w{3}) (?P<val>[+-]\d+)$')

program = []
for line in lines:
    match = pattern.match(line)
    input_dict = match.groupdict()
    instruction = {
        "inst": input_dict["inst"],
        "val": int(input_dict["val"]),
        "hit": False
    }
    program.append(instruction)


def run_program(program: list):
    # Reset program
    for instruction in program:
        instruction["hit"] = False
    acc = 0
    pc = 0
    while pc < len(program) and not program[pc]["hit"]:
        program[pc]["hit"] = True
        inst = program[pc]["inst"]
        val = program[pc]["val"]
        print("acc: {} pc: {} -> inst: {} val: {}".format(acc, pc, inst, val))
        if inst == "acc":
            acc += val
            pc += 1
        elif inst == "nop":
            pc += 1
        elif inst == "jmp":
            pc += val
        else:
            print("Unknown command!: " + inst)

    return(acc, pc)


# Part 01:
(acc, pc) = run_program(program)
print("Part 01: instruction re-hit")
print("acc: {}, pc: {}".format(acc, pc))

for mod_pos in range(len(program)):
    print("--- Run {} ---".format(mod_pos))

    mod_inst = program[mod_pos]
    # Mod instruction (or skip)
    if mod_inst["inst"] == "acc":
        print("Skipping")
        continue
    if mod_inst["inst"] == "nop":
        print("Modding nop instruction at {} to jmp".format(mod_pos))
        mod_inst["inst"] = "jmp"
    elif mod_inst["inst"] == "jmp":
        print("Modding jmp instruction at {} to nop".format(mod_pos))
        mod_inst["inst"] = "nop"

    # Run program
    (acc, pc) = run_program(program)
    print("Results: acc: {}, pc: {}".format(acc, pc))
    if pc >= len(program):
        break

    # Reset instruction
    if mod_inst["inst"] == "nop":
        mod_inst["inst"] = "jmp"
    elif mod_inst["inst"] == "jmp":
        mod_inst["inst"] = "nop"

print("Part 02:")
print("acc: {}, pc: {}".format(acc, pc))
print("-------------")

# for instruction in program:
#     print(str(instruction))
