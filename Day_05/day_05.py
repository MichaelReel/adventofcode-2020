#!/env/python3

text_file = open("Day_05/input", "r")
lines = [x.strip() for x in text_file.readlines()]

max_pos_id = int('1111111111', 2)

# Part 01
highest_id = 0
lowest_id = max_pos_id
for line in lines:
    line = line.replace('F', '0')
    line = line.replace('L', '0')
    line = line.replace('B', '1')
    line = line.replace('R', '1')
    _id = int(line, 2)
    highest_id = max(highest_id, _id)
    lowest_id = min(lowest_id, _id)

print("Part 01: Highest ID: " + str(highest_id))

# Part 02
ids_found = [False] * max_pos_id
for line in lines:
    line = line.replace('F', '0')
    line = line.replace('L', '0')
    line = line.replace('B', '1')
    line = line.replace('R', '1')
    id = int(line, 2)
    ids_found[id] = True

for id in range(lowest_id, highest_id + 1):
    if not ids_found[id]:
        print("Part 02: ID not found: " + str(id))
