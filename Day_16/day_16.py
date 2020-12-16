#!/env/python3

import re

text_file = open("Day_16/input", "r")
ticket_info = [x.strip() for x in text_file.readlines()]

# Part 01
range_1_re = r'(?P<r1s>\d+)-(?P<r1e>\d+)'
range_2_re = r'(?P<r2s>\d+)-(?P<r2e>\d+)'
field_re = r'^(?P<name>.*):\s' + range_1_re + r'\sor\s' + range_2_re + r'$'
field_pattern = re.compile(field_re)

fields = {}
pos = 0
valid_all = set()
for ind, line in enumerate(ticket_info):
    if line == '':
        pos = ind
        break
    line_match = field_pattern.match(line)
    line_dict = line_match.groupdict()
    fields[line_dict['name']] = line_dict
    range_1 = range(int(line_dict['r1s']), int(line_dict['r1e']) + 1)
    range_2 = range(int(line_dict['r2s']), int(line_dict['r2e']) + 1)
    fields[line_dict['name']]['valid'] = set(range_1).union(range_2)

    valid_all = valid_all.union(range_1)
    valid_all = valid_all.union(range_2)

for ind, line in enumerate(ticket_info[pos:]):
    if line == 'your ticket:':
        pos += ind + 1
        break
my_ticket = [int(x) for x in ticket_info[pos].split(',')]

for ind, line in enumerate(ticket_info[pos:]):
    if line == 'nearby tickets:':
        pos += ind + 1
        break

other_tickets = []
failure_total = 0
for line in ticket_info[pos:]:
    ticket = [int(x) for x in line.split(',')]
    failure = False
    for value in ticket:
        if value not in valid_all:
            failure_total += value
            failure = True
    if not failure:
        other_tickets.append(ticket)

print("Part 01: ticket scanning error rate: " + str(failure_total))

# Starting with all fields as valid for each column and eliminate
valid_fields = []
for _ in range(len(fields)):
    valid_fields.append(list(fields.keys()))

# Remove field names that can't be true for a given ticket index
for ticket in other_tickets:
    for field in fields.values():
        for val_ind in range(len(valid_fields)):
            if ticket[val_ind] not in field['valid']:
                if field['name'] in valid_fields[val_ind]:
                    valid_fields[val_ind].remove(field['name'])

# If a field has only one possibility, remove it from the rest of the lists
unsolved = list(range(len(valid_fields)))
while len(unsolved) > 0:
    for val_ind in range(len(valid_fields)):
        if val_ind not in unsolved:
            continue
        if len(valid_fields[val_ind]) == 1:
            field_name = valid_fields[val_ind][0]
            for oth_ind in unsolved:
                if oth_ind != val_ind and field_name in valid_fields[oth_ind]:
                    valid_fields[oth_ind].remove(field_name)
            unsolved.remove(val_ind)

# Get the 'departure' fields and the multiplied values
field_names = [item for sublist in valid_fields for item in sublist]
departure_multi = 1
for i, field_name in enumerate(field_names):
    if field_name.startswith('departure '):
        print("{}: {}".format(field_name, my_ticket[i]))
        departure_multi *= my_ticket[i]

print("Part 02: Multiplied departure values: {}".format(departure_multi))
