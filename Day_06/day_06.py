#!/env/python3

text_file = open("Day_06/input", "r")
lines = [x.strip() for x in text_file.readlines()]

# Part 01
concat_lines = []
concat_line = ""

for line in lines:
    if len(line) == 0:
        concat_lines.append(dict.fromkeys(concat_line))
        concat_line = ""
    else:
        concat_line += line
concat_lines.append(dict.fromkeys(concat_line))

total = 0
for concat_line in concat_lines:
    total += len(concat_line)

print("Part 01: Total: " + str(total))

# Part 02
merge_lines = []
merge_line = set()
passengers = 0

for line in lines:
    if len(line) == 0:
        merge_lines.append(merge_line)
        merge_line = set()
        passengers = 0
    else:
        if passengers == 0:
            merge_line = set(line)
        else:
            merge_line = merge_line.intersection(line)
        passengers += 1
merge_lines.append(merge_line)

total = 0
for merge_line in merge_lines:
    total += len(merge_line)

print("Part 02: Total: " + str(total))
