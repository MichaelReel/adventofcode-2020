#!/env/python3

import re


text_file = open("Day_02/input", "r")
lines = [x for x in text_file.readlines()]

# Part 01
regex = r'^(?P<min>\d+)-(?P<max>\d+)\s(?P<char>[a-z]):\s(?P<pass>[a-z]+)$'
parse_line = re.compile(regex)
passes = 0
fails = 0
for line in lines:
    m = parse_line.match(line)
    if not m:
        print("Didn't match: " + line)

    line_data = m.groupdict()
    char_count = line_data["pass"].count(line_data["char"])
    char_min = int(line_data["min"])
    char_max = int(line_data["max"])
    if char_count >= char_min and char_count <= char_max:
        passes += 1
    else:
        fails += 1

print("{} passes and {} fails".format(passes, fails))

# Part 02
regex = r'^(?P<pos_a>\d+)-(?P<pos_b>\d+)\s(?P<char>[a-z]):\s(?P<pass>[a-z]+)$'
parse_line = re.compile(regex)
passes = 0
fails = 0
for line in lines:
    m = parse_line.match(line)
    if not m:
        print("Didn't match: " + line)

    line_data = m.groupdict()

    char_a = line_data["pass"][int(line_data["pos_a"]) - 1]
    char_b = line_data["pass"][int(line_data["pos_b"]) - 1]

    if ((line_data["char"] == char_a) ^ (line_data["char"] == char_b)):
        passes += 1
    else:
        fails += 1

print("{} passes and {} fails".format(passes, fails))
