#!/env/python3

preamble_len = 25
text_file = open("Day_10/input", "r")
jolts = sorted([int(x.strip()) for x in text_file.readlines()])

device_joltage = max(jolts) + 3
jolts.append(device_joltage)

# print("device_joltage: {}".format(device_joltage))
# print("adapters: " + str(jolts))

# Part 01
one_jolt_devices = 0
three_jolt_devices = 0
other_jolt_devices = 0
previous = 0

for device in jolts:
    if device - previous == 3:
        three_jolt_devices += 1
    elif device - previous == 1:
        one_jolt_devices += 1
    else:
        other_jolt_devices += 1
    previous = device

# print(
#     "ones: {}, threes: {}, others: {}".format(
#         one_jolt_devices,
#         three_jolt_devices,
#         other_jolt_devices
#     )
# )
print("Part 01: Test output: " + str(one_jolt_devices * three_jolt_devices))

# Put a zero at the start
jolts.insert(0, 0)

tree_desc = []
# paths = 1
for ind in range(len(jolts)):
    valid_range = range(ind + 1, min(ind + 4, len(jolts)))
    inds_in_range = [x for x in valid_range if jolts[x] <= jolts[ind] + 3]
    tree_desc.append({"val": jolts[ind], "children": inds_in_range})

# Set the final path position
tree_desc[-1]["paths"] = 1

# Work back and count extra paths
for ind in range(len(tree_desc) - 2, -1, -1):
    paths = 0
    for sub_ind in tree_desc[ind]["children"]:
        paths += tree_desc[sub_ind]["paths"]
    tree_desc[ind]["paths"] = paths
    # print("[" + str(ind) + "] " + str(tree_desc[ind]))

print("Part 02: Possible arrangements: " + str(tree_desc[0]["paths"]))
