from abc import ABC, abstractmethod
from typing import List, Tuple, TypeVar, Iterable
import numpy
import time
import random


Move = TypeVar('Move')
Node = TypeVar('Node')


class Problem(ABC):
    @abstractmethod
    def print(self) -> None:
        pass

    @abstractmethod
    def is_done(self) -> bool:
        pass

    @abstractmethod
    def get_next_node(self) -> Node:
        pass

    @abstractmethod
    def get_next_nodes(self, length: int) -> List[Node]:
        pass

    @abstractmethod
    def load_next_nodes(self, node) -> None:
        pass

    @abstractmethod
    def get_moves(self, node: Node) -> Iterable[Move]:
        pass

    @abstractmethod
    def has_moves(self, node: Node) -> bool:
        pass

    @abstractmethod
    def move(self, move: Move, node: Node):
        pass

    @abstractmethod
    def back(self, move: Move, node: Node):
        pass

    @abstractmethod
    def rate_move(self, move: Move):
        pass


class CSP:
    def __init__(self, problem: Problem):
        self.problem = problem
        self.visits = 0

    def back_tracking(self, log=False):
        self.visits += 1
        problem = self.problem
        if problem.is_done():
            return True
        result = False
        node = problem.get_next_node()
        possible = problem.get_moves(node)
        # possible = sorted(possible, key=lambda move: problem.rate_move(move))
        random.shuffle(possible)
        if log:
            print('Node:' + str(node))
            print('Possible:' + str(possible))
            self.problem.print()
            input()
        for move in possible:
            problem.load_next_nodes(node)
            problem.move(move, node)
            result = self.back_tracking(log)
            if result:
                break
            problem.back(move, node)
        return result

    def forward_checking(self, max_insight):
        self.visits += 1
        problem = self.problem
        if problem.is_done():
            return True
        result = False
        node = problem.get_next_node()
        possible = problem.get_moves(node)
        # possible = sorted(possible, key=lambda move: problem.rate_move(move))
        random.shuffle(possible)
        for move in possible:
            problem.load_next_nodes(node)
            problem.move(move, node)
            forward_check = (problem.has_moves(node) for node in problem.get_next_nodes(max_insight))
            if False not in forward_check:
                result = self.forward_checking(max_insight)
            if result:
                break
            problem.back(move, node)
        return result


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
        return self.nexts[self.index:length]

    def load_next_nodes(self, node):
        self.nexts += [adj for adj in self.adjacent_nodes(node) if adj not in self.nexts]

    def get_moves(self, node: Tuple[int, int]) -> List[int]:
        return [color for color in range(1, self.colors + 1) if self.check_move(color, self.adjacent_colors(node))]

    def has_moves(self, node: Tuple[int, int]) -> bool:
        return any(self.get_moves(node))

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


def test1():
    current_milli_time = lambda: int(round(time.time() * 1000))
    print("Size:\tBT iters:\t\tBT time:\t\tFC iters:\t\tFC time")
    for i in range(2, 8):
        init = (int(i/2), int(i/2))
        log = str(i) + "\t"
        problem1 = Crate(i, init)
        problem2 = Crate(i, init)
        csp1 = CSP(problem1)
        timer = current_milli_time()
        csp1.back_tracking()
        timer = current_milli_time() - timer
        log += str(csp1.visits) + "\t\t" + str(timer) + "\t\t"
        csp2 = CSP(problem2)
        timer = current_milli_time()
        csp2.forward_checking(i * 2)
        timer = current_milli_time() - timer
        log += str(csp2.visits) + "\t\t" + str(timer) + "\t\t"
        print(log)

def test2():
    problem = Crate(3)
    csp = CSP(problem)
    csp.back_tracking(log=True)

for i in range(5):
    test1()