#!/env/python3

import re

text_file = open("Day_14/input", "r")
mem_instructions = [x.strip() for x in text_file.readlines()]

# Part 01
and_mask = int('111111111111111111111111111111111111', 2)
or_mask = int('000000000000000000000000000000000000', 2)
memory = {}

mask_pattern = r'mask\s=\s(?P<mask>[X01]{36})'
mem_pattern = r'mem\[(?P<pos>\d+)\]\s=\s(?P<val>\d+)'
inst_pattern = re.compile(r'^(?:' + mask_pattern + r'|' + mem_pattern + r')$')
inst_list = []

for inst in mem_instructions:
    inst_match = inst_pattern.match(inst)
    inst_list.append(inst_match.groupdict())

for inst_match in inst_list:
    if inst_match["mask"]:
        and_mask = int(inst_match["mask"].replace('X', '1'), 2)
        or_mask = int(inst_match["mask"].replace('X', '0'), 2)
    elif inst_match["pos"] and inst_match["val"]:
        pos = int(inst_match["pos"])
        val = (int(inst_match["val"]) | or_mask) & and_mask
        memory[pos] = val

mem_sum = sum(memory.values())
print("Part 01: Sum of memory: " + str(mem_sum))


# Part 02
full_mask = '111111111111111111111111111111111111'


def get_mem_positions(pos: int, mask: str) -> set:
    mem_addresses = set()
    # Mask position first
    pos |= int(mask.replace('X', '0'), 2)
    mem_addresses.add(pos)
    # Figure out floating positions
    for i, bit in enumerate(reversed(mask)):
        if bit == 'X':
            new_pos = set()
            for mem_pos in mem_addresses:
                or_pos = mem_pos | (1 << i)
                and_pos = mem_pos & ~(1 << i)
                new_pos.add(or_pos)
                new_pos.add(and_pos)
            mem_addresses = mem_addresses.union(new_pos)

    # print("Returning addresses: " + str(mem_addresses))
    return mem_addresses


memory = {}
current_mask = '000000000000000000000000000000000000'
for inst_match in inst_list:
    if inst_match["mask"]:
        current_mask = inst_match["mask"]
    elif inst_match["pos"] and inst_match["val"]:
        val = int(inst_match["val"])
        for pos in get_mem_positions(int(inst_match["pos"]), current_mask):
            memory[pos] = val

mem_sum = sum(memory.values())

print("Part 02: Sum of memory: " + str(mem_sum))
