#!/env/python3

text_file = open("Day_12/input", "r")
ship_instructions = [x.strip() for x in text_file.readlines()]


class Vector():
    x: int
    y: int

    def __init__(self, _x: int, _y: int):
        self.x = _x
        self.y = _y

    def add(self, movement):
        self.x += movement.x
        self.y += movement.y
        # print("Adding movement: {}".format(movement))

    def rotate_cw(self, degrees: int):
        for _i in range(int(degrees / 90)):
            new_y = self.x * -1
            new_x = self.y
            self.x = new_x
            self.y = new_y

    def rotate_ccw(self, degrees: int):
        for _i in range(int(degrees / 90)):
            new_x = self.y * -1
            new_y = self.x
            self.x = new_x
            self.y = new_y

    def multiply(self, distance: int):
        return Vector(self.x * distance, self.y * distance)

    def manhattan(self) -> int:
        return abs(self.x) + abs(self.y)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)


# Part 01
facing = Vector(1, 0)
position = Vector(0, 0)
for instruction in ship_instructions:
    cmd = instruction[0]
    value = int(instruction[1:])

    if cmd == 'N':
        position.add(Vector(0, value))
    elif cmd == 'S':
        position.add(Vector(0, -value))
    elif cmd == 'E':
        position.add(Vector(value, 0))
    elif cmd == 'W':
        position.add(Vector(-value, 0))
    elif cmd == 'F':
        position.add(facing.multiply(value))
    elif cmd == 'R':
        facing.rotate_cw(value)
    elif cmd == 'L':
        facing.rotate_ccw(value)

print(
    "Part 01: Position = {}, Manhattan distance = {}".format(
        position, position.manhattan()
    )
)

# Part 02
waypoint = Vector(10, 1)
position = Vector(0, 0)
for instruction in ship_instructions:
    cmd = instruction[0]
    value = int(instruction[1:])

    if cmd == 'N':
        waypoint.add(Vector(0, value))
    elif cmd == 'S':
        waypoint.add(Vector(0, -value))
    elif cmd == 'E':
        waypoint.add(Vector(value, 0))
    elif cmd == 'W':
        waypoint.add(Vector(-value, 0))
    elif cmd == 'F':
        position.add(waypoint.multiply(value))
    elif cmd == 'R':
        waypoint.rotate_cw(value)
    elif cmd == 'L':
        waypoint.rotate_ccw(value)

print(
    "Part 02: Position = {}, Waypoint = {}, Manhattan distance = {}".format(
        position, waypoint, position.manhattan()
    )
)
