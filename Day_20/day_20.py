#!/env/python3

text_file = open("Day_20/input", "r")
lines = [x.strip() for x in text_file.readlines()]


class Connection:
    # _edge1
    # _edge2

    def __init__(self, edge1, edge2):
        self._edge1 = edge1
        self._edge2 = edge2

    def get_other_edge(self, edge):
        if self._edge1 == edge:
            return self._edge2
        if self._edge2 == edge:
            return self._edge1
        return None

    def __str__(self):
        return "conn ({}) => ({})".format(self._edge1, self._edge2)


class Edge:
    # _tile
    _value: int
    _inverse: int
    _side: str
    _connection: Connection

    def __init__(self, tile, edge_str, side):
        self._tile = tile
        binary_string = edge_str.replace('.', '0').replace('#', '1')
        self._value = int(binary_string, 2)
        self._inverse = int(binary_string[::-1], 2)
        self._side = side
        self._connection = None

    def tile(self) -> object:
        return self._tile

    def value(self) -> int:
        return self._value

    def matches(self, other) -> bool:
        return other.value() == self._value or other.value() == self._inverse

    def has_connection(self) -> bool:
        return self._connection is not None

    def set_connection(self, connection):
        self._connection = connection

    def connect_to(self, other) -> Connection:
        connection = Connection(self, other)
        self.set_connection(connection)
        other.set_connection(connection)
        return connection

    def get_connected_tile(self):
        if self._connection is None:
            return None
        return self._connection.get_other_edge(self).tile()

    def __str__(self):
        tile_name = self._tile.name()
        side = self._tile.get_edge_side(self)
        val = self._value
        inv = self._inverse
        desc = "{} of {}: {}/{}".format(side, tile_name, val, inv)

        return desc


class Tile:
    _name: int
    _data: list
    _edges: dict
    _connections: list

    def __init__(self, name, data):
        self._name = name
        self._data = data
        self._create_edge_data()
        self._connections = []

    def name(self):
        return self._name

    def _create_edge_data(self):
        """
        Create an edge object for each (Top Left Right Bottom) edge
        """
        self._edges = {}

        # Get the edge strings and make edge objects
        left_str = ''.join([x[0] for x in self._data])
        right_str = ''.join([x[-1] for x in self._data])
        self._edges['top'] = Edge(self, self._data[0], 'top')
        self._edges['bottom'] = Edge(self, self._data[-1], 'bottom')
        self._edges['left'] = Edge(self, left_str, 'left')
        self._edges['right'] = Edge(self, right_str, 'right')

    def edges(self) -> list:
        return self._edges.values()

    def get_edge_match(self, other_edge: Edge) -> Edge:
        for edge in self._edges.values():
            if edge.matches(other_edge):
                return edge
        return None

    def get_edge_side(self, edge: Edge) -> str:
        for edge_side in self._edges.keys():
            if self._edges[edge_side] == edge:
                return edge_side
        return ''

    def add_connection(self, connection: Connection):
        self._connections.append(connection)

    def perform_edge_comparison(self, other_tile):
        """
        Update the current tile with data to indicate if it can connect to the
        other and return any connection established
        """
        connection = None
        for edge in self._edges.values():
            if edge.has_connection():
                continue
            other_edge = other_tile.get_edge_match(edge)
            if other_edge is not None:
                #  Create connection between edges and also record in each tile
                connection = edge.connect_to(other_edge)
                self.add_connection(connection)
                other_tile.add_connection(connection)
        return connection

    def is_border(self) -> bool:
        return len(self._connections) == 3

    def is_corner(self) -> bool:
        return len(self._connections) == 2

    def is_top_left(self) -> bool:
        if not self.is_corner():
            return False
        top = self._edges['bottom'].has_connection()
        left = self._edges['right'].has_connection()
        return top and left

    def has_downward_tile(self) -> bool:
        return self._edges['bottom'].has_connection()

    def get_downward_tile(self) -> object:
        down_edge = self._edges['bottom']
        return down_edge.get_connected_tile()

    def has_rightward_tile(self) -> bool:
        return self._edges['right'].has_connection()

    def get_rightward_tile(self) -> object:
        right_edge = self._edges['right']
        return right_edge.get_connected_tile()

    def find_connection_from_list(self, names: list) -> object:
        """ Find the first tile connected to this one, thats also in names """
        for edge in self._edges.values():
            other_tile = edge.get_connected_tile()
            if other_tile and other_tile.name() in names:
                return other_tile

    def all_connected_names_from_list(self, names: list) -> list:
        """ Return all the names in the list this tile connects to """
        connected_tiles = []
        for edge in self._edges.values():
            other_tile = edge.get_connected_tile()
            if other_tile and other_tile.name() in names:
                connected_tiles.append(other_tile.name())
        return connected_tiles

    def get_direction_of_tile(self, tile: object) -> str:
        """ Return the direction key for this tile """
        for direction in self._edges.keys():
            edge = self._edges[direction]
            other_tile = edge.get_connected_tile()
            if other_tile == tile:
                return direction
        return ''

    def rotate_90_cw(self):
        """ Rotate all the data by 90 degrees and update the edges """
        # Rotate data
        new_data = []
        for ind in range(len(self._data[0])):
            new_data.append(''.join([x[ind] for x in self._data[::-1]]))
        self._data = new_data
        # Rotate edges
        old_up = self._edges['top']
        self._edges['top'] = self._edges['left']
        self._edges['left'] = self._edges['bottom']
        self._edges['bottom'] = self._edges['right']
        self._edges['right'] = old_up

    def flip_horizontally(self):
        """ Reverse all the data and update edges """
        # Reverse data
        for ind in range(len(self._data)):
            self._data[ind] = self._data[ind][::-1]
        # Reverse edges
        old_left = self._edges['left']
        self._edges['left'] = self._edges['right']
        self._edges['right'] = old_left

    def flip_vertically(self):
        """ Reverse all the data and update edges """
        # Reverse data
        self._data = self._data[::-1]
        # Reverse edges
        old_up = self._edges['top']
        self._edges['top'] = self._edges['bottom']
        self._edges['bottom'] = old_up

    def get_internal_data_dimensions(self) -> (int, int):
        y = len(self._data) - 2
        x = len(self._data[0]) - 2
        return x, y

    def get_internal_data_row(self, index) -> str:
        return self._data[index + 1][1:-1]

    def pattern_is_at(self, pattern, start_x, start_y) -> bool:
        for pat_y in range(len(pattern)):
            for pat_x in range(len(pattern[0])):
                if pattern[pat_y][pat_x] != ' ':
                    data_x = pat_x + start_x
                    data_y = pat_y + start_y
                    datum = self._data[data_y][data_x]
                    if pattern[pat_y][pat_x] != datum:
                        return False
        return True

    def clear_pattern_at(self, pattern, start_x, start_y):
        for pat_y in range(len(pattern)):
            for pat_x in range(len(pattern[0])):
                if pattern[pat_y][pat_x] != ' ':
                    data_x = pat_x + start_x
                    data_y = pat_y + start_y
                    row_list = list(self._data[data_y])
                    row_list[data_x] = 'O'
                    self._data[data_y] = ''.join(row_list)

    def get_all_occurrences_of_pattern(self, pattern) -> list:
        match_list = []
        max_y = len(self._data) - len(pattern) + 1
        max_x = len(self._data[0]) - len(pattern[0]) + 1
        for y in range(max_y):
            for x in range(max_x):
                if self.pattern_is_at(pattern, x, y):
                    match_list.append({'x': x, 'y': y})
        return match_list

    def count_occurrences_of_pattern(self, pattern) -> int:
        occurrences = self.get_all_occurrences_of_pattern(pattern)
        return len(occurrences)

    def rotate_until_pattern_found(self, monster):
        for ind in range(4):
            if self.count_occurrences_of_pattern(monster) > 0:
                return
            self.rotate_90_cw()
        self.flip_horizontally()
        for ind in range(4):
            if self.count_occurrences_of_pattern(monster) > 0:
                return
            self.rotate_90_cw()

    def remove_all_occurrences_of_pattern(self, pattern):
        positions = self.get_all_occurrences_of_pattern(pattern)
        for pos in positions:
            self.clear_pattern_at(pattern, pos['x'], pos['y'])

    def __str__(self):
        left = '----'
        top = '----'
        bottom = '----'
        right = '----'
        if 'left' in self._edges:
            left_tile = self._edges['left'].get_connected_tile()
            if left_tile:
                left = left_tile.name()
        if 'top' in self._edges:
            top_tile = self._edges['top'].get_connected_tile()
            if top_tile:
                top = top_tile.name()
        if 'bottom' in self._edges:
            bottom_tile = self._edges['bottom'].get_connected_tile()
            if bottom_tile:
                bottom = bottom_tile.name()
        if 'right' in self._edges:
            right_tile = self._edges['right'].get_connected_tile()
            if right_tile:
                right = right_tile.name()

        return "[{}<{}^({})v{}>{}]".format(
            left, top, self._name, bottom, right
        )


class TileArray:
    _tiles: dict
    _edges: list
    _connections: list
    _border_tile_names: list
    _corner_tile_names: list
    _internal_tile_names: list
    _tile_grid: list

    def __init__(self):
        self._tiles = {}
        self._edges = []
        self._connections = []
        self._border_tile_names = []
        self._corner_tile_names = []
        self._internal_tile_names = []
        self._tile_grid = []

    def add_tile(self, tile: Tile):
        self._tiles[tile.name()] = tile
        self._edges += tile.edges()

    def perform_edge_comparisons(self):
        for tile in self._tiles.values():
            for other in self._tiles.values():
                if other == tile:
                    continue
                connection = tile.perform_edge_comparison(other)
                if connection is not None:
                    self._connections.append(connection)

        # While we're here, find the corners and borders
        for tile in self._tiles.values():
            if tile.is_border():
                self._border_tile_names.append(tile.name())
            elif tile.is_corner():
                self._corner_tile_names.append(tile.name())
            else:
                self._internal_tile_names.append(tile.name())

    def corner_product(self) -> int:
        """ Part 01 """
        corner_product = 1
        for corner in self._corner_tile_names:
            corner_product *= corner
        return corner_product

    def establish_tile_grid(self):
        """ Arrange the tiles in a grid by connections """
        # Nominate 1 corner as the source of top-left source of truth
        top_left = self._tiles[self._corner_tile_names[0]]
        for corner in self._corner_tile_names:
            if self._tiles[corner].is_top_left():
                top_left = self._tiles[corner]

        # Process border tiles downwards until we reach another corner
        border_names = [] + self._border_tile_names
        corner_names = [] + self._corner_tile_names
        corner_names.remove(top_left.name())

        # Create the top row
        self._tile_grid.append([top_left.name()])

        # (This only works if the top_left corner is orientated:)
        border_tile = top_left.get_downward_tile()

        # Create a new row for each border tile going downwards
        while border_tile and border_tile.name() in border_names:
            self._tile_grid.append([border_tile.name()])
            border_names.remove(border_tile.name())
            down_tile = border_tile.find_connection_from_list(border_names)
            if down_tile is None:
                break
            border_tile = down_tile

        # Create the bottom row
        bottom_left = border_tile.find_connection_from_list(corner_names)
        corner_names.remove(bottom_left.name())
        self._tile_grid.append([bottom_left.name()])

        # Populate the top border row, similar to how we did the left column
        border_tile = top_left.get_rightward_tile()
        while border_tile and border_tile.name() in border_names:
            self._tile_grid[0].append(border_tile.name())
            border_names.remove(border_tile.name())
            right_tile = border_tile.find_connection_from_list(border_names)
            if right_tile is None:
                break
            border_tile = right_tile

        top_right = border_tile.find_connection_from_list(corner_names)
        corner_names.remove(top_right.name())
        self._tile_grid[0].append(top_right.name())

        # The rest of the grid now has reference tiles to establish connections
        tile_bank = self._internal_tile_names + border_names + corner_names

        for y in range(1, len(self._tile_grid)):
            for x in range(1, len(self._tile_grid[0])):
                up_tile = self._tiles[self._tile_grid[y - 1][x]]
                left_tile = self._tiles[self._tile_grid[y][x - 1]]
                up_list = up_tile.all_connected_names_from_list(tile_bank)
                this_tile = left_tile.find_connection_from_list(up_list)
                if this_tile is None:
                    print("Something not correct at ({},{})".format(x, y))
                self._tile_grid[y].append(this_tile.name())
                tile_bank.remove(this_tile.name())

    def perform_tile_alignment(self):
        """ Flip/Rotate tiles to line up all the tiles correctly """

        # Align each tile in the left column to the one above
        # Flip horizontally if the right connection is pointing left
        for y in range(1, len(self._tile_grid)):
            tile = self._tiles[self._tile_grid[y][0]]
            up_tile = self._tiles[self._tile_grid[y - 1][0]]
            # Which connection should be up?
            side = tile.get_direction_of_tile(up_tile)
            while side != 'top':
                tile.rotate_90_cw()
                side = tile.get_direction_of_tile(up_tile)
            # If there is no right tile, flip horizontally
            if not tile.has_rightward_tile():
                tile.flip_horizontally()

        # Align each tile in the top row to the one to the left
        # Flip vertically if the bottom connection is pointing up
        for x in range(1, len(self._tile_grid[0])):
            tile = self._tiles[self._tile_grid[0][x]]
            left_tile = self._tiles[self._tile_grid[0][x - 1]]
            # Which connection should be left?
            side = tile.get_direction_of_tile(left_tile)
            while side != 'left':
                tile.rotate_90_cw()
                side = tile.get_direction_of_tile(left_tile)
            # If there is no down tile, flip vertically
            if not tile.has_downward_tile():
                tile.flip_vertically()

        # Align each remaining tile, rotate until up is up, flip if left isn't
        for y in range(1, len(self._tile_grid)):
            for x in range(1, len(self._tile_grid[0])):
                tile = self._tiles[self._tile_grid[y][x]]
                up_tile = self._tiles[self._tile_grid[y - 1][x]]
                left_tile = self._tiles[self._tile_grid[y][x - 1]]
                # Which connection should be up?
                side = tile.get_direction_of_tile(up_tile)
                while side != 'top':
                    tile.rotate_90_cw()
                    side = tile.get_direction_of_tile(up_tile)
                # If the left tile isn't correct, flip it
                if tile.get_direction_of_tile(left_tile) != 'left':
                    tile.flip_horizontally()

    def create_super_tile(self) -> Tile:
        super_data = []
        top_left = self._tiles[self._tile_grid[0][0]]
        int_dim_x, int_dim_y = top_left.get_internal_data_dimensions()
        for tile_row in self._tile_grid:
            for data_row in range(int_dim_y):
                data_line = ''
                for tile_name in tile_row:
                    tile = self._tiles[tile_name]
                    data_line += tile.get_internal_data_row(data_row)
                super_data.append(data_line)
        return Tile(0, super_data)

    def __str__(self):
        desc = ''
        for tile_row in self._tile_grid:
            for tile_name in tile_row:
                desc += str(self._tiles[tile_name])
            desc += '\n'

        return desc


tiles = TileArray()
line_pos = 0
while line_pos < len(lines):
    if lines[line_pos].startswith("Tile"):
        tile_name = int(lines[line_pos][5:-1])
        tile_data = []
        line_pos += 1
        while line_pos < len(lines) and lines[line_pos]:
            tile_data.append(lines[line_pos])
            line_pos += 1
        tiles.add_tile(Tile(tile_name, tile_data))
    line_pos += 1

tiles.perform_edge_comparisons()
print("Part 01: Product of corner tiles: {}".format(tiles.corner_product()))

tiles.establish_tile_grid()
tiles.perform_tile_alignment()
super_tile = tiles.create_super_tile()

# Search for the monster pattern, counting occurrences
# Rotate and flip the tile through all permutations
monster = [
    '                  # ',
    '#    ##    ##    ###',
    ' #  #  #  #  #  #   ',
]

super_tile.rotate_until_pattern_found(monster)

# # Can actually assume they don't overlap so this would be enough:
#
# total_hashes = super_tile.count_occurrences_of_pattern(['#'])
# monsters = super_tile.count_occurrences_of_pattern(monster)
# monster_hashes = monsters * 15  # Hashes in monster pattern above
# roughness = total_hashes - monster_hashes

# To be extra pedantic, accommodate overlaps
super_tile.remove_all_occurrences_of_pattern(monster)
roughness = super_tile.count_occurrences_of_pattern(['#'])

# for row in super_tile._data:
#     print(row)

print("Part 02: Roughness: {}".format(roughness))
