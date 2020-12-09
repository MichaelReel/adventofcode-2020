#!/env/python3

preamble_len = 25
text_file = open("Day_09/input", "r")
lines = [int(x.strip()) for x in text_file.readlines()]


# Part 01
def sum_in_preamble(num, preamble) -> bool:
    sum_found = False
    for ind_a in range(len(preamble)):
        for ind_b in range(ind_a + 1, len(preamble)):
            a = preamble[ind_a]
            b = preamble[ind_b]
            # print("Test {} + {} = {} == {}".format(a, b, a + b, num))
            if a + b == num:
                sum_found = True
                break
        if sum_found:
            break

    return sum_found


for ind in range(len(lines) - preamble_len - 1):
    next_num = lines[ind + preamble_len]
    preamble = lines[ind:ind + preamble_len]
    sum_found = sum_in_preamble(next_num, preamble)
    # print("{}:{}:{}".format(str(preamble), str(next_num), str(sum_found)))

    if not sum_found:
        print("Part 01: No sum found: " + str(next_num))
        break


# Part 02
def find_contiguous_sum(num, input_list) -> (int, int):
    start_ind = -1
    end_ind = -1
    for ind_a in range(len(input_list)):
        cont_sum = input_list[ind_a]
        ind_b = ind_a + 1
        while cont_sum < num:
            cont_sum += input_list[ind_b]
            ind_b += 1
        if cont_sum == num:
            start_ind = ind_a
            end_ind = ind_b
            break
    return (start_ind, end_ind)


(start_ind, end_ind) = find_contiguous_sum(next_num, lines)
print("Found contiguous sum: start: {}, end: {}".format(start_ind, end_ind))
print(str(lines[start_ind:end_ind]))
sum_min_max = min(lines[start_ind:end_ind]) + max(lines[start_ind:end_ind])
print("Part 02: Sum of min max in contiguous list: {}".format(sum_min_max))
