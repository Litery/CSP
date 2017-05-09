from typing import List, Tuple
import numpy
import random
from Abstracts import Problem


class Crate(Problem):
    def __init__(self, size: int, init=(0, 0)):
        self.size = size
        self.colors = 2 * size
        self.crate = numpy.zeros((size, size), dtype="int_")
        if size % 2 is not 0:
            self.colors += 1
        self.nexts = [init]
        self.used = numpy.zeros((self.colors, self.colors), dtype="int_")
        self.index = 0

    def print(self):
        print("Nexts: " + str(self.nexts[self.index:]))
        numpy.set_printoptions(precision=0, formatter={'int': lambda x: '{:02}'.format(x) if x != 0 else "--"})
        for row in self.crate:
            print(row)
        for row in self.used:
            print(row)

    def is_done(self):
        return 0 not in self.crate

    def get_next_node(self):
        return self.nexts[self.index]

    def get_next_nodes(self, length: int) -> List[Tuple[int, int]]:
        return self.nexts[self.index: self.index + length]

    def load_next_nodes(self, node):
        self.nexts += [adj for adj in self.adjacent_nodes(node) if adj not in self.nexts]

    def get_moves(self, node: Tuple[int, int]) -> List[int]:
        return [color for color in range(1, self.colors + 1) if self.check_move(color, self.adjacent_colors(node))]

    def have_moves(self, depth: int) -> bool:
        return False not in [any(self.get_moves(node)) for node in self.get_next_nodes(depth)]

    def move(self, move: int, node: Tuple[int, int]):
        self.crate[node] = move
        for color in self.adjacent_colors(node):
            if color >= move:
                self.used[color - 1][move - 1] = 1
            else:
                self.used[move - 1][color - 1] = 1
        self.index += 1

    def back(self, move: int, node: Tuple[int, int]):
        self.crate[node] = 0
        for color in self.adjacent_colors(node):
            if color >= move:
                self.used[color - 1][move - 1] = 0
            else:
                self.used[move - 1][color - 1] = 0
        self.index -= 1

    def rate_move(self, move: int):
        result = 0
        for x in range(self.colors - 1):
            result += self.used[(x, move - 1)]
            result += self.used[(move - 1, x)]
        return (result) / (self.colors - 1)

    def adjacent_nodes(self, node: Tuple[int, int]):
        (x, y) = node
        out = (-1, self.size)
        return [(x, y) for x, y in [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)] if
                x not in out and y not in out]

    def adjacent_colors(self, node: Tuple[int, int]):
        result = [self.crate[(x, y)] for x, y in self.adjacent_nodes(node) if self.crate[(x, y)] != 0]
        return result

    def check_move(self, move, adjacent) -> bool:
        for color in adjacent:
            if move >= color and self.used[move - 1][color - 1] == 1:
                return False
            elif self.used[color - 1][move - 1] == 1:
                return False
            elif move in adjacent:
                return False
        return True
