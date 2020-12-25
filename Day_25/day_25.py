#!/env/python3

text_file = open("Day_25/input", "r")
public_keys = [int(x.strip()) for x in text_file.readlines()]


def try_loop_subject(loop: int, subject: int):
    value = 1
    for i in range(loop):
        value *= subject
        value %= 20201227
    return value


def find_loop_values(subject: int, public_keys: list):
    key_loop = {}
    value = subject
    loop_num = 1
    while len(key_loop) < len(public_keys):
        value *= subject
        value %= 20201227
        loop_num += 1
        if value in public_keys:
            key_loop[value] = loop_num
    return key_loop


key_loops = find_loop_values(7, public_keys)
key_1 = try_loop_subject(key_loops[public_keys[0]], public_keys[1])
key_2 = try_loop_subject(key_loops[public_keys[1]], public_keys[0])

if (key_1 == key_2):
    print("Part 01: encryption key: " + str(key_1))
