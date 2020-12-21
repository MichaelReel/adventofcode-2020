#!/env/python3

import re

text_file = open("Day_21/input", "r")
lines = [x.strip() for x in text_file.readlines()]

food_re = r'^(?P<ingredients>[^(]*)\s\(contains\s(?P<allergens>[^)]*)\)$'
food_pattern = re.compile(food_re)

allergen_table = {}
all_ingredients = {}
for line in lines:
    food_match = food_pattern.match(line)
    if not food_match:
        print("Regex didn't match line: " + line)

    food_dict = food_match.groupdict()
    ingredients = set(food_dict['ingredients'].split(' '))
    allergens = set(food_dict['allergens'].split(', '))

    for allergen in allergens:
        if allergen not in allergen_table:
            allergen_table[allergen] = ingredients
        else:
            ingrets = ingredients.intersection(
                allergen_table[allergen]
            )
            allergen_table[allergen] = ingrets

    for ingredient in ingredients:
        if ingredient not in all_ingredients:
            all_ingredients[ingredient] = 1
        else:
            all_ingredients[ingredient] += 1

# Part 01
count = 0
for ingredient in all_ingredients.keys():
    associated = False
    for ingredient_list in allergen_table.values():
        if ingredient in ingredient_list:
            associated = True
    if not associated:
        count += all_ingredients[ingredient]

print("Part 01: non-allergen ingredients appears {} times".format(count))

# Part 02
# Where an allergen has 1 ingredient,
# remove the ingredient from the other allergens
allergen_map = {}
while len(allergen_table) > 0:
    drop_list = []
    for allergen in allergen_table.keys():
        if len(allergen_table[allergen]) == 1:
            ingredient = allergen_table[allergen].pop()
            drop_list.append(allergen)
            allergen_map[allergen] = ingredient
            for other_allergen in allergen_table.keys():
                if ingredient in allergen_table[other_allergen]:
                    allergen_table[other_allergen].remove(ingredient)
    for drop in drop_list:
        del allergen_table[drop]

danger_list = ''

for allergen in sorted(allergen_map.keys()):
    danger_list += ",{}".format(allergen_map[allergen])

print("Part 02: Dangerous allergens list: {}".format(danger_list[1:]))
