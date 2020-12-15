#!/env/python3

spoken = [15, 5, 1, 4, 7, 0]

# Part 01 (Approach 1: Slower)
while len(spoken) <= 2019:
    prev_index = len(spoken)
    number = spoken[-1]
    if number not in spoken[0:-1]:
        spoken.append(0)
    else:
        turn = (len(spoken) - 1) - (spoken[:-1])[::-1].index(number)
        age = prev_index - turn
        spoken.append(age)

print("Part 01: 2020th number: {}".format(spoken[2019]))

# Part 02 (Approach 2: A little more efficient)
last_spoken = {}
for i, s in enumerate(spoken[:-1]):
    last_spoken[s] = i + 1

number = spoken[-1]
for turn in range(len(spoken), 30000000):
    # if not turn % 3000000:
    #     print(str(turn * 100 / 30000000) + "%")
    last_turn = last_spoken[number] if number in last_spoken else 0
    age = turn - last_turn if last_turn else 0
    last_spoken[number] = turn
    number = age

print("Part 02: 30000000th number: {}".format(number))
