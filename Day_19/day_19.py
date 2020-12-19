#!/env/python3

import re

text_file = open("Day_19/input", "r")
lines = [x.strip() for x in text_file.readlines()]

rule_re = re.compile(r'^(?P<name>\d+):\s(?P<rule>.*)$')

rule_lines = [
    rule_re.match(line).groupdict()
    for line in lines
    if rule_re.match(line)
]
rules = {rule['name']: rule for rule in rule_lines}
messages = [line for line in lines[len(rules):] if line]

# For 'Part 02' I introduced this filthy hack:
#   Basically, looped regexes are simply expanded up to `traversal_limit`.
#   `traversal_limit` is an arbitrary limit found by "experimentation",
#   (i.e.: raise the value and rerun until the result stops changing).
#
#   Totally not proud of this. I only did it because I'd started with regex
#   and didn't want to rewrite everything again.

traversal_limit = 6  # Absolute totally filthy hack


def normalise_rule(rules, name) -> str:
    # Don't bother if we've already normalised
    if 're' in rules[name]:
        return rules[name]['re']

    # If literal, that's enough
    if rules[name]['rule'][0] == '"':
        rules[name]['re'] = rules[name]['rule'].strip('"')
        return rules[name]['re']

    # If this rule is already being traversed, we have a loop
    if 'traversed' in rules[name]:
        rules[name]['traversed'] += 1
        # We'll have 2 rule parts, one with and one without a self reference
        if rules[name]['traversed'] >= traversal_limit:
            return ''
    else:
        # Mark current rule as being traversed
        rules[name]['traversed'] = 1

    # If references, get each reference as literal
    # If '|' we need to create a group
    pre = '(?:' if '|' in rules[name]['rule'] else ''
    post = ')' if '|' in rules[name]['rule'] else ''

    # Step through references and build re
    re = pre
    for token in rules[name]['rule'].split(' '):
        if token == '|':
            re += '|'
        else:
            re += normalise_rule(rules, token)
    re += post
    rules[name]['re'] = re
    rules[name]['traversed'] -= 1
    if rules[name]['traversed'] <= 0:
        del rules[name]['traversed']
    return re


for name in rules.keys():
    normalise_rule(rules, name)

# print("Rules: \n" + "\n".join([str(rule) for rule in rules.values()]))

rule_0 = re.compile('^' + rules['0']['re'] + '$')
match_count = 0
for message in messages:
    if rule_0.match(message):
        match_count += 1
    #     print(message + ": matches")
    # else:
    #     print(message + ": doesn't match")

print("Part 01: {} messages match rule 0".format(match_count))

for name in rules.keys():
    del rules[name]['re']

rules['8'] = {'name': '8', 'rule': '42 | 42 8'}
rules['11'] = {'name': '11', 'rule': '42 31 | 42 11 31'}

for name in rules.keys():
    normalise_rule(rules, name)

# print("Rules: \n" + "\n".join([str(rule) for rule in rules.values()]))

rule_0 = re.compile('^' + rules['0']['re'] + '$')
match_count = 0
for message in messages:
    if rule_0.match(message):
        match_count += 1
    #     print(message + ": matches")
    # else:
    #     print(message + ": doesn't match")

print("Part 02: {} messages match rule 0".format(match_count))
