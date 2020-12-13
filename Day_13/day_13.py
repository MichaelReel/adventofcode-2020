#!/env/python3

import math

text_file = open("Day_13/input", "r")
bus_timings = [x.strip() for x in text_file.readlines()]

# Part 01
timestamp = int(bus_timings[0])
buses = [int(x) for x in bus_timings[1].split(',') if x != 'x']

print("{}: {}".format(timestamp, str(buses)))

next_bus = 0
next_time = timestamp + max(buses) + 1

for bus in buses:
    recent_trips = int(timestamp / bus)
    this_bus_time = (recent_trips + 1) * bus
    if this_bus_time < next_time:
        next_time = this_bus_time
        next_bus = bus

wait_time = next_time - timestamp
print(
    "Can get bus {} at time {}, waiting {}".format(
        next_bus, next_time, wait_time
    )
)
print("Part 01: Wait time by bus: " + str(wait_time * next_bus))


# Part 02
def time_is_contest_result(timestamp: int, bus_offsets: list) -> bool:
    for bus_offset in bus_offsets:
        if (timestamp + bus_offset["pos"]) % bus_offset["bus"] != 0:
            return False
    return True


bus_inputs = bus_timings[1].split(',')
bus_offsets = []
pos = 0

for bus_in in bus_inputs:
    if bus_in != 'x':
        bus = int(bus_in)
        bus_offsets.append(
            {
                "bus": bus,
                "pos": pos,
            }
        )
    pos += 1

bus_offsets = sorted(bus_offsets, key=lambda k: k['bus'], reverse=True)
timestamp = -bus_offsets[0]["pos"]
current_jump = bus_offsets[0]["bus"]

best_match_ind = -1

for sub_ind in range(1, len(bus_offsets) + 1):
    sub_list = bus_offsets[:sub_ind]
    while not time_is_contest_result(timestamp, sub_list):
        timestamp += current_jump
    # We've found a point were some buses align. Increment faster!
    current_jump = math.prod([x["bus"] for x in sub_list])

print("Part 02: Contest Solution: " + str(timestamp))
