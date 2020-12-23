#!/env/python3

# cup_input = list('389125467')  # Test
cup_input = list('586439172')  # Real


class Cup:
    _label: int
    _next: object

    def __init__(self, label: int):
        self._label = label

    def set_next(self, next_cw: object):
        self._next = next_cw

    def next(self) -> object:
        return self._next

    def label(self) -> int:
        return self._label

    def __str__(self):
        return str(self._label)

    __repr__ = __str__


class CupGame:
    _cup_ref: dict
    _current: Cup
    _str_start: Cup
    _max_label: Cup

    def __init__(self, cup_input: list):
        self._cup_ref = {}
        in_list = []
        self._max_label = 0
        for cup_label in [int(x) for x in cup_input]:
            cup = Cup(cup_label)
            if in_list:
                in_list[-1].set_next(cup)
            in_list.append(cup)
            self._cup_ref[cup_label] = cup
            self._max_label = max(self._max_label, cup_label)
        in_list[-1].set_next(in_list[0])
        self._current = in_list[0]
        self._str_start = in_list[0]

    def __str__(self):
        out_string = ''
        cup = self._str_start
        while cup.next() != self._str_start:
            if cup == self._current:
                out_string += " ({})".format(cup)
            else:
                out_string += " {}".format(cup)
            cup = cup.next()
        if cup == self._current:
            out_string += " ({})".format(cup)
        else:
            out_string += " {}".format(cup)
        return out_string

    def _pop_next_cup(self) -> Cup:
        cup = self._current.next()
        self._current.set_next(cup.next())
        return cup

    def _push_next_cup(self, dest: Cup, insert: Cup):
        insert.set_next(dest.next())
        dest.set_next(insert)

    def _get_destination_label(self, pick_list: list):
        dest_label = self._current.label() - 1
        if dest_label < 1:
            dest_label = self._max_label

        while dest_label in [x.label() for x in pick_list]:
            dest_label -= 1
            if dest_label < 1:
                dest_label = self._max_label

        return dest_label

    def perform_move(self):
        pick_up = []
        for _ in range(3):
            pick_up.append(self._pop_next_cup())

        dest_label = self._get_destination_label(pick_up)
        dest_cup = self._cup_ref[dest_label]
        for insert_cup in pick_up[::-1]:
            self._push_next_cup(dest_cup, insert_cup)

        self._current = self._current.next()

    def labels_after_1(self) -> str:
        cup = self._cup_ref[1]
        start_cup = cup
        out_string = ''
        while cup.next() != start_cup:
            cup = cup.next()
            out_string += str(cup.label())
        return out_string

    def next_2_labels(self) -> list:
        cup = self._cup_ref[1]
        return [cup.next().label(), cup.next().next().label()]

    def insert_cups_to_1000000(self):
        min_cup = self._max_label
        last_placed = self._current
        while last_placed.next() != self._current:
            last_placed = last_placed.next()

        for ind in range(1000000, min_cup, -1):
            cup = Cup(ind)
            self._push_next_cup(last_placed, cup)
            self._cup_ref[ind] = cup
            self._max_label = max(self._max_label, ind)


# Part 01
moves = 100
cup_game = CupGame(cup_input)
for _ in range(moves):
    cup_game.perform_move()

print("Part 01: cup labels: {}".format(cup_game.labels_after_1()))

# Part 02
moves = 10000000
cup_game = CupGame(cup_input)
cup_game.insert_cups_to_1000000()
for move in range(moves):
    if (move + 1) % 100000 == 0:
        print(str(int((move + 1) / 100000)) + "%", end='\r')
    cup_game.perform_move()

star_cups = cup_game.next_2_labels()
product = star_cups[0] * star_cups[1]
print("Part 02: Star-Cup product: {}".format(product))
