#!/env/python3


target_sum = 2020
text_file = open("Day_01/input", "r")
values = [int(x) for x in text_file.readlines()]

# Part 01
for index in range(len(values)):
    value = values[index]
    for other_value in values[index:]:
        if value + other_value == target_sum:
            print(str(value) + "+" + str(other_value) + "=" + str(target_sum))
            product = value * other_value
            print(str(value) + "*" + str(other_value) + "=" + str(product))

# Part 02
for ind_a, val_a in enumerate(values):
    for ind_b, val_b in enumerate(values[ind_a + 1:], ind_a + 1):
        for ind_c, val_c in enumerate(values[ind_b + 1:], ind_b + 1):
            if val_a + val_b + val_c == target_sum:
                print(str(val_a) + "+" + str(val_b) + "+" + str(val_c) + "=" + str(target_sum))
                product = val_a * val_b * val_c
                print(str(val_a) + "*" + str(val_b) + "*" + str(val_c) + "=" + str(product))
