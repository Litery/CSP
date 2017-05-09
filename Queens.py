import numpy
from typing import Tuple, List
from Abstracts import Problem


def gen_dir():
    result = []
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            yield (x, y)


class Queens(Problem):
    def __init__(self, size, init):
        self.size = size
        self.crate = numpy.zeros((size, size), dtype="int_")
        self.nexts = [init]
        self.index = 0
        pass

    def print(self):
        print("Nexts: " + str(self.nexts[self.index:]))
        numpy.set_printoptions(precision=0, formatter={'int': lambda x: '{:02}'.format(x) if x != 0 else "--"})
        for row in self.crate:
            print(row)

    def have_moves(self, depth: int) -> bool:
        if depth == 0 or len(self.nexts) < self.size * self.size:
            return True
        result = numpy.sum(self.crate)
        for node in self.nexts[self.index: -1]:
            result += sum(self.get_moves(node))
            if result == self.size:
                return True
        return False

    def get_moves(self, node: Tuple[int, int]) -> List[int]:
        if False in (self.check_conflicts(node, dire) for dire in gen_dir() if dire != (0, 0)):
            return [0]
        else:
            return [1, 0]

    def load_next_nodes(self, node: Tuple[int, int]) -> None:
        self.nexts += [adj for adj in self.adjacent_nodes(node) if adj not in self.nexts]

    def rate_move(self, move: int):
        return 1

    def move(self, move: int, node: Tuple[int, int]):
        self.crate[node] = move
        self.index += 1

    def back(self, move: int, node: Tuple[int, int]):
        self.crate[node] = 0
        self.index -= 1

    def get_next_node(self) -> Tuple[int, int]:
        return self.nexts[self.index] if self.index < len(self.nexts) else None

    def get_next_nodes(self, length: int):
        return self.nexts[self.index: self.index + length]

    def is_done(self) -> bool:
        return numpy.count_nonzero(self.crate) == self.size

    def adjacent_nodes(self, node: Tuple[int, int]):
        (x, y) = node
        out = (-1, self.size)
        return [(x, y) for x, y in [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)] if
                x not in out and y not in out]

    def check_conflicts(self, node, direction):
        (x, y) = node
        out = (-1, self.size)
        (x, y) = (x + direction[0], y + direction[1])
        while x not in out and y not in out:
            if self.crate[(x, y)] == 1:
                return False
            (x, y) = (x + direction[0], y + direction[1])
        return True