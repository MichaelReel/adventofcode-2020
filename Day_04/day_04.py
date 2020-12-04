#!/env/python3

import re


text_file = open("Day_04/input", "r")
lines = [x.strip() for x in text_file.readlines()]

concat_lines = []
concat_line = ""

for line in lines:
    if len(line) == 0:
        concat_lines.append(concat_line)
        concat_line = ""
    else:
        concat_line += " " + line
concat_lines.append(concat_line)

credential_list = []
for line in concat_lines:
    credentials = {}
    line = line.strip()
    for pair_str in line.split(' '):
        key, value = pair_str.split(':')
        credentials[key] = value
    credential_list.append(credentials)

# Part 01
expected_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
valid_creds = 0
for credentials in credential_list:
    okay = True
    for field in expected_fields:
        if field not in credentials:
            okay = False
    if okay:
        valid_creds += 1
    #     print("OKAY: " + str(credentials))
    # else:
    #     print("BAD : " + str(credentials))

print("Part 01: " + str(valid_creds) + " valid creds")


hgt_regex = re.compile(r'^(?P<height>\d{2,3})(?P<units>cm|in)$')
hcl_regex = re.compile(r'^\#[0-9a-f]{6}$')
ecl_regex = re.compile(r'^(?:amb|blu|brn|gry|grn|hzl|oth)$')
pid_regex = re.compile(r'^\d{9}$')

valid_creds = 0
for credentials in credential_list:
    print("TRY : " + str(credentials))
    okay = True
    for field in expected_fields:
        if field not in credentials:
            print("Missing field: " + field)
            okay = False
            continue

    if not okay:
        print("Fields missing")
        continue

    byr = int(credentials["byr"])
    if byr < 1920 or byr > 2002:
        continue

    iyr = int(credentials["iyr"])
    if iyr < 2010 or iyr > 2020:
        continue

    eyr = int(credentials["eyr"])
    if eyr < 2020 or eyr > 2030:
        continue

    hgt_match = hgt_regex.match(credentials["hgt"])
    if not hgt_match:
        continue

    hgt_dict = hgt_match.groupdict()
    units = hgt_dict["units"]
    height = int(hgt_dict["height"])
    if units == 'in' and (height < 59 or height > 76):
        continue
    if units == 'cm' and (height < 150 or height > 193):
        continue

    hcl_match = hcl_regex.match(credentials["hcl"])
    if not hcl_match:
        continue

    ecl_match = ecl_regex.match(credentials["ecl"])
    if not ecl_match:
        continue

    pid_match = pid_regex.match(credentials["pid"])
    if not pid_match:
        continue

    valid_creds += 1
    print("OKAY: " + str(credentials))

print("Part 02: " + str(valid_creds) + " valid creds")
