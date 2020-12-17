#!/env/python3

text_file = open("Day_17/input", "r")
z_0_info = [x.strip() for x in text_file.readlines()]


# Part 01:
class PocketDimensionState():
    cube: dict
    bounds: dict = {
        'x': {'lower': 0, 'upper': 0},
        'y': {'lower': 0, 'upper': 0},
        'z': {'lower': 0, 'upper': 0},
    }

    def __init__(self, z_0_info: list):
        self.cube = {}
        self.cube[0] = {}
        for y, row in enumerate(z_0_info):
            self.cube[0][y] = {}
            for x, cell in enumerate(row):
                self.set_cell(x, y, 0, cell)

    def __str__(self):
        str_out = ''
        bds = self.bounds
        for z in range(bds['z']['lower'], bds['z']['upper'] + 1):
            str_out += "z={}\n".format(z)
            for y in range(bds['y']['lower'], bds['y']['upper'] + 1):
                for x in range(bds['x']['lower'], bds['x']['upper'] + 1):
                    str_out += '#' if self.is_cell_active(x, y, z) else '.'
                str_out += "\n"
            str_out += "\n"
        return str_out

    def is_cell_active(self, x, y, z) -> bool:
        if z not in self.cube:
            return False
        if y not in self.cube[z]:
            return False
        if x not in self.cube[z][y]:
            return False
        return self.cube[z][y][x] == '#'

    def get_cell_score(self, x, y, z):
        if z not in self.cube:
            return 0
        if y not in self.cube[z]:
            return 0
        if x not in self.cube[z][y]:
            return 0
        return self.cube[z][y][x]

    def _update_bounds(self, x, y, z):
        """Bounds are purely for beautifying the __str__ method"""
        bds = self.bounds
        for n, v in [('x', x), ('y', y), ('z', z)]:
            bds[n]['lower'] = min(bds[n]['lower'], v)
            bds[n]['upper'] = max(bds[n]['upper'], v)

    def set_cell(self, x, y, z, data):
        self._update_bounds(x, y, z)
        if z not in self.cube:
            self.cube[z] = {}
        if y not in self.cube[z]:
            self.cube[z][y] = {}
        self.cube[z][y][x] = data

    def inc_cell_neighbors(self, x_mid: int, y_mid: int, z_mid: int):
        for z in range(z_mid - 1, z_mid + 2):
            for y in range(y_mid - 1, y_mid + 2):
                for x in range(x_mid - 1, x_mid + 2):
                    if x == x_mid and y == y_mid and z == z_mid:
                        continue
                    score = self.get_cell_score(x, y, z) + 1
                    self.set_cell(x, y, z, score)

    def apply_automata_rules(self, old, x, y, z):
        active = old.is_cell_active(x, y, z)
        score = self.get_cell_score(x, y, z)
        if active:
            if score >= 2 and score <= 3:
                self.set_cell(x, y, z, '#')
            else:
                self.set_cell(x, y, z, '.')
        else:
            if score == 3:
                self.set_cell(x, y, z, '#')
            else:
                self.set_cell(x, y, z, '.')

    def cycle(self):
        new = PocketDimensionState([])

        # Propagate outwards - create cells with neighbor counts first
        for z in self.cube.keys():
            for y in self.cube[z].keys():
                for x in self.cube[z][y].keys():
                    if self.is_cell_active(x, y, z):
                        new.inc_cell_neighbors(x, y, z)

        # Convert all cell scores by the rules
        for z in new.cube.keys():
            for y in new.cube[z].keys():
                for x in new.cube[z][y].keys():
                    new.apply_automata_rules(self, x, y, z)
        return new

    def count_active_cubes(self):
        count = 0
        for z in self.cube.keys():
            for y in self.cube[z].keys():
                for x in self.cube[z][y].keys():
                    if self.is_cell_active(x, y, z):
                        count += 1
        return count


state = PocketDimensionState(z_0_info)
print("\nBefore any cycles:\n")
print(str(state))

for i in range(6):
    state = state.cycle()
    print("\nAfter {} cycle{}:\n".format(i + 1, 's' if i > 0 else ''))
    print(str(state))


# Part 02
class FourDimensionState():
    cube: dict
    bounds: dict = {
        'x': {'lower': 0, 'upper': 0},
        'y': {'lower': 0, 'upper': 0},
        'z': {'lower': 0, 'upper': 0},
        'w': {'lower': 0, 'upper': 0},
    }

    def __init__(self, w_z_0_info: list):
        self.cube = {}
        self.cube[0] = {}
        self.cube[0][0] = {}
        for y, row in enumerate(w_z_0_info):
            self.cube[0][0][y] = {}
            for x, cell in enumerate(row):
                self.set_cell(x, y, 0, 0, cell)

    def __str__(self):
        str_out = ''
        bds = self.bounds
        justify = (bds['y']['upper'] - bds['y']['lower']) + 3
        for w in range(bds['w']['lower'], bds['w']['upper'] + 1):
            str_out += "w={}\n".format(w)
            for z in range(bds['z']['lower'], bds['z']['upper'] + 1):
                str_out += "z={}".format(z, w).ljust(justify)
            str_out += "\n"
            for y in range(bds['y']['lower'], bds['y']['upper'] + 1):
                for z in range(bds['z']['lower'], bds['z']['upper'] + 1):
                    x_l = ''
                    for x in range(bds['x']['lower'], bds['x']['upper'] + 1):
                        x_l += '#' if self.is_cell_active(x, y, z, w) else '.'
                    str_out += x_l.ljust(justify)
                str_out += "\n"
        return str_out

    def is_cell_active(self, x, y, z, w) -> bool:
        if w not in self.cube:
            return False
        if z not in self.cube[w]:
            return False
        if y not in self.cube[w][z]:
            return False
        if x not in self.cube[w][z][y]:
            return False
        return self.cube[w][z][y][x] == '#'

    def get_cell_score(self, x, y, z, w):
        if w not in self.cube:
            return 0
        if z not in self.cube[w]:
            return 0
        if y not in self.cube[w][z]:
            return 0
        if x not in self.cube[w][z][y]:
            return 0
        return self.cube[w][z][y][x]

    def _update_bounds(self, x, y, z, w):
        """Bounds are purely for beautifying the __str__ method"""
        bds = self.bounds
        for n, v in [('x', x), ('y', y), ('z', z), ('w', w)]:
            bds[n]['lower'] = min(bds[n]['lower'], v)
            bds[n]['upper'] = max(bds[n]['upper'], v)

    def set_cell(self, x, y, z, w, data):
        self._update_bounds(x, y, z, w)
        if w not in self.cube:
            self.cube[w] = {}
        if z not in self.cube[w]:
            self.cube[w][z] = {}
        if y not in self.cube[w][z]:
            self.cube[w][z][y] = {}
        self.cube[w][z][y][x] = data

    def inc_cell_neighbors(self, x_m: int, y_m: int, z_m: int, w_m: int):
        for w in range(w_m - 1, w_m + 2):
            for z in range(z_m - 1, z_m + 2):
                for y in range(y_m - 1, y_m + 2):
                    for x in range(x_m - 1, x_m + 2):
                        if x == x_m and y == y_m and z == z_m and w == w_m:
                            continue
                        score = self.get_cell_score(x, y, z, w) + 1
                        self.set_cell(x, y, z, w, score)

    def apply_automata_rules(self, old, x, y, z, w):
        active = old.is_cell_active(x, y, z, w)
        score = self.get_cell_score(x, y, z, w)
        if active:
            if score >= 2 and score <= 3:
                self.set_cell(x, y, z, w, '#')
            else:
                self.set_cell(x, y, z, w, '.')
        else:
            if score == 3:
                self.set_cell(x, y, z, w, '#')
            else:
                self.set_cell(x, y, z, w, '.')

    def cycle(self):
        new = FourDimensionState([])

        # Propagate outwards - create cells with neighbor counts first
        for w in self.cube.keys():
            for z in self.cube[w].keys():
                for y in self.cube[w][z].keys():
                    for x in self.cube[w][z][y].keys():
                        if self.is_cell_active(x, y, z, w):
                            new.inc_cell_neighbors(x, y, z, w)

        # Convert all cell scores by the rules
        for w in new.cube.keys():
            for z in new.cube[w].keys():
                for y in new.cube[w][z].keys():
                    for x in new.cube[w][z][y].keys():
                        new.apply_automata_rules(self, x, y, z, w)
        return new

    def count_active_cubes(self):
        count = 0
        for w in self.cube.keys():
            for z in self.cube[w].keys():
                for y in self.cube[w][z].keys():
                    for x in self.cube[w][z][y].keys():
                        if self.is_cell_active(x, y, z, w):
                            count += 1
        return count


four_dimension_state = FourDimensionState(z_0_info)
print("\nBefore any cycles:\n")
print(str(four_dimension_state))

for i in range(6):
    four_dimension_state = four_dimension_state.cycle()
    print("\nAfter {} cycle{}:\n".format(i + 1, 's' if i > 0 else ''))
    print(str(four_dimension_state))

# Print both results last

print(
    "Part 01: Pocket dimension six-cycle cubes active: {}".format(
        state.count_active_cubes()
    )
)

print(
    "Part 02: Four dimension six-cycle cubes active: {}".format(
        four_dimension_state.count_active_cubes()
    )
)
