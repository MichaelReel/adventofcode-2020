#!/env/python3

import re

text_file = open("Day_07/input", "r")
lines = [x.strip() for x in text_file.readlines()]

bag_rules = {}
bag_key_regex = re.compile(r'^(?P<color>.*) bags contain (?P<contents>.*)$')
content_regex = re.compile(r'^(?:, )?(?P<count>\d+) (?P<color>[^,.]*) bags?')

for line in lines:
    bag_match = bag_key_regex.match(line)
    if not bag_match:
        print("BAD LINE: " + line)
        continue
    bag_rule = bag_match.groupdict()

    # print(str(bag_rule))

    contents = bag_rule["contents"]
    content_rules = {}
    content_match = content_regex.match(contents)
    while content_match:
        content_rule = content_match.groupdict()
        # print(str(content_rule))
        content_rules[content_rule["color"]] = content_rule["count"]
        contents = content_regex.sub("", contents)
        content_match = content_regex.match(contents)

    bag_rules[bag_rule["color"]] = content_rules

# print(str(bag_rules))

inverted_bag_rules = {}

for bag_key in bag_rules:
    for content_key in bag_rules[bag_key]:
        if content_key not in inverted_bag_rules:
            inverted_bag_rules[content_key] = []
        inverted_bag_rules[content_key].append(bag_key)

# print(str(inverted_bag_rules))


# Part 01:
def get_containers(color, rules) -> int:
    all_containers = set([])
    container_list = rules[color]
    all_containers = all_containers.union(container_list)
    del rules[color]
    for container in container_list:
        if container in rules:
            sub_contents = get_containers(container, rules)
            all_containers = all_containers.union(sub_contents)
    return all_containers


start_color = 'shiny gold'
all_containing_colors = get_containers(start_color, inverted_bag_rules)
print("Part 01: containing bags: " + str(len(all_containing_colors)))


# Part 02:
def get_content_count(color) -> int:
    total = 0
    for content_color in bag_rules[color]:
        bag_count = int(bag_rules[color][content_color])
        total += bag_count
        total += bag_count * get_content_count(content_color)
    return total


need_contents = str(get_content_count('shiny gold'))
print("Part 02: Must contain " + need_contents + " other bags")
