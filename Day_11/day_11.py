#!/env/python3

text_file = open("Day_11/input", "r")
row_descs = [x.strip() for x in text_file.readlines()]


class Seating:
    seat_rows = []

    def __init__(self, seat_description: list):
        self.seat_rows = seat_description

    def get_adjacent_occupied_seats(self, mid_x, mid_y) -> int:
        count = 0
        y_min = max(mid_y - 1, 0)
        y_max = min(mid_y + 2, len(self.seat_rows))
        y_range = range(y_min, y_max)

        # debug = ""
        for y in y_range:
            x_min = max(mid_x - 1, 0)
            x_max = min(mid_x + 2, len(self.seat_rows[y]))
            x_range = range(x_min, x_max)

            for x in x_range:
                # debug += "({},{})".format(x, y)
                if x == mid_x and y == mid_y:
                    continue
                if self.seat_rows[y][x] == "#":
                    count += 1

        # print("({},{}): {} : {}".format(mid_x, mid_y, count, debug))
        return count

    def get_p1_rule_for_seat(self, x, y) -> str:
        if self.seat_rows[y][x] == "L":
            if self.get_adjacent_occupied_seats(x, y) == 0:
                return "#"
            else:
                return "L"
        if self.seat_rows[y][x] == "#":
            if self.get_adjacent_occupied_seats(x, y) >= 4:
                return "L"
            else:
                return "#"
        return self.seat_rows[y][x]

    def perform_p1_sitting_rules(self):
        new_seat_rows = []
        for y in range(len(self.seat_rows)):
            seat_row = self.seat_rows[y]
            new_seat_row = ""
            for x in range(len(seat_row)):
                new_seat = self.get_p1_rule_for_seat(x, y)
                new_seat_row += new_seat
            new_seat_rows.append(new_seat_row)
        return Seating(new_seat_rows)

    def find_seat_occupied_in_dir(self, start_x, start_y, dx, dy) -> bool:
        x = start_x + dx
        y = start_y + dy
        while (
            y >= 0 and y < len(self.seat_rows) and
            x >= 0 and x < len(self.seat_rows[y])
        ):
            if self.seat_rows[y][x] == "#":
                return True
            elif self.seat_rows[y][x] == "L":
                return False
            x += dx
            y += dy
        return False

    def get_lines_of_sight_occupied(self, mid_x, mid_y) -> int:
        dir_list = [
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, -1),
            (-1, 0),
            (-1, 1)
        ]
        count = 0
        for (dx, dy) in dir_list:
            if self.find_seat_occupied_in_dir(mid_x, mid_y, dx, dy):
                count += 1
        return count

    def get_p2_rule_for_seat(self, x, y):
        if self.seat_rows[y][x] == "L":
            if self.get_lines_of_sight_occupied(x, y) == 0:
                return "#"
            else:
                return "L"
        if self.seat_rows[y][x] == "#":
            if self.get_lines_of_sight_occupied(x, y) >= 5:
                return "L"
            else:
                return "#"
        return self.seat_rows[y][x]

    def perform_p2_sitting_rules(self):
        new_seat_rows = []
        for y in range(len(self.seat_rows)):
            seat_row = self.seat_rows[y]
            new_seat_row = ""
            for x in range(len(seat_row)):
                new_seat = self.get_p2_rule_for_seat(x, y)
                new_seat_row += new_seat
            new_seat_rows.append(new_seat_row)
        return Seating(new_seat_rows)

    def __str__(self):
        string = ""
        for row in self.seat_rows:
            string += row + "\n"
        return string

    def count_occupied(self):
        return sum([x.count('#') for x in self.seat_rows])


# Part 01
prev_seating = Seating(row_descs)
seating = prev_seating.perform_p1_sitting_rules()

while seating.count_occupied() != prev_seating.count_occupied():
    prev_seating = seating
    seating = prev_seating.perform_p1_sitting_rules()

# print("\n" + str(seating))
print("Part 01: Seat's Occupied: " + str(seating.count_occupied()))

# Part 02
prev_seating = Seating(row_descs)
seating = prev_seating.perform_p2_sitting_rules()

while seating.count_occupied() != prev_seating.count_occupied():
    prev_seating = seating
    seating = prev_seating.perform_p2_sitting_rules()

# print("\n" + str(seating))
print("Part 02: Seat's Occupied: " + str(seating.count_occupied()))
