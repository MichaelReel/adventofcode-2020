#!/env/python3

import re

text_file = open("Day_24/input", "r")
lines = [x.strip() for x in text_file.readlines()]

dir_pattern = re.compile(r'(?:nw|sw|ne|se|w|e)')
flip_lists = [dir_pattern.findall(line) for line in lines]

# A hex grid can be represented as a square grid with movement on 1 diagonal
#                                |
#         [nw]      [ne]         |     [nw]      [ne]
#                                |
#     [w]       []       [e]     |      [w]       []       [e]
#                                |
#         [sw]      [se]         |               [sw]      [se]

orig = (0, 0)
dir_map = {
    'nw': (-1, -1),
    'ne': (0, -1),
    'w': (-1,  0),
    'e': (1,  0),
    'sw': (0,  1),
    'se': (1,  1),
}


def add(tup1: (int, int), tup2: (int, int)) -> (int, int):
    return (tup1[0] + tup2[0], tup1[1] + tup2[1])


tile_map = {}  # This could probably be a set
# Follow each instruction path and 'flip' the destination tile
for flip_list in flip_lists:
    pos = orig
    for dir_inst in flip_list:
        pos = add(pos, dir_map[dir_inst])
    if pos in tile_map:
        del tile_map[pos]
    else:
        tile_map[pos] = True

print("Part 01: Black side up tiles: {}".format(len(tile_map)))


def cellular_automata(in_tiles: dict) -> dict:
    dirs = list(dir_map.values())
    tiles_score = {}
    # For each tile in the in-list, give to it's neighbors score
    for tile in in_tiles:
        for t_dir in dirs:
            pos = add(tile, t_dir)
            if pos in tiles_score:
                tiles_score[pos] += 1
            else:
                tiles_score[pos] = 1

    # For each 'scored' tile, check if it's black or white and create new map
    out_tiles = {}
    for tile in tiles_score:
        if tile in in_tiles:
            # Black tile
            if tiles_score[tile] >= 1 and tiles_score[tile] <= 2:
                out_tiles[tile] = True
        else:
            # White tile
            if tiles_score[tile] == 2:
                out_tiles[tile] = True

    return out_tiles


for i in range(1, 101):
    tile_map = cellular_automata(tile_map)

print("Part 02: Black side up tiles: {}".format(len(tile_map)))
