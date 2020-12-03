#!/env/python3

import re


text_file = open("Day_03/input", "r")
lines = [x.strip() for x in text_file.readlines()]

# Part 01
traverse = {"x": 3, "y": 1}
pos = {"x": 0, "y": 0}
trees = 0
while pos["y"] < (len(lines) - 1):
    pos["x"] += traverse["x"]
    pos["y"] += traverse["y"]
    line = lines[pos["y"]]
    mod_x = pos["x"] % (len(line))
    terrain = line[mod_x]
    if (terrain == '#'):
        trees += 1
    print("{}: {}".format(str(pos), terrain))
print("Part 01: Trees encountered: " + str(trees) + "\n\n")

# Part 02
traverses = [
    {"x": 1, "y": 1},
    {"x": 3, "y": 1},
    {"x": 5, "y": 1},
    {"x": 7, "y": 1},
    {"x": 1, "y": 2},
]
product = 1
for traverse in traverses:
    pos = {"x": 0, "y": 0}
    trees = 0
    while pos["y"] < (len(lines) - 1):
        pos["x"] += traverse["x"]
        pos["y"] += traverse["y"]
        line = lines[pos["y"]]
        mod_x = pos["x"] % (len(line))
        terrain = line[mod_x]
        if (terrain == '#'):
            trees += 1
        # print("{}: {}".format(str(pos), terrain))
    print("Trees encountered: " + str(trees))
    product *= trees
print("Trees Product: " + str(product))