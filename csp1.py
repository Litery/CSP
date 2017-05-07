from abc import ABC, abstractmethod
from typing import List, Tuple
from copy import deepcopy
import numpy


class Move(ABC):
    pass


class State(ABC):
    @abstractmethod
    def add_next(self, next: List[Move]):
        pass

    def has_next(self) -> bool:
        pass

    def get_next_move(self) -> Move:
        pass

    @abstractmethod
    def move(self, move: Move):
        pass

    @abstractmethod
    def back(self, move: Move, **kwargs):
        pass

    @abstractmethod
    def filter_moves(self, moves: List[Move], **kwargs) -> bool:
        pass


class Problem(ABC):
    @abstractmethod
    def is_done(self) -> bool:
        pass

    @abstractmethod
    def get_next(self, pos: Move) -> List[Move]:
        pass

    @abstractmethod
    def get_moves(self, move: Move) -> List[Move]:
        pass

    @abstractmethod
    def move(self, move: Move):
        pass

    @abstractmethod
    def back(self, move: Move):
        pass

    @abstractmethod
    def get_state(self) -> State:
        pass


class CrateMove(Move):
    def __init__(self, pos: Tuple[int, int], color=-1):
        self.position = pos
        self.color = color


class CrateState(State):
    def __init__(self, size: int, nexts: List[CrateMove]):
        self.nexts: List[CrateMove] = nexts
        self.move_index: int = 0
        self.used = numpy.zeros((size, size), dtype="int_")

    def add_next(self, next_elements: List[Move]):
        self.nexts += next_elements

    def has_next(self):
        return self.move_index < len(self.nexts)

    def in_next(self, pos: Tuple[int, int]):
        return any(x.position == pos for x in self.nexts)

    def get_next_move(self):
        return self.nexts[self.move_index]

    def move(self, move: CrateMove, **kwargs):
        adjacent: List[int] = kwargs.get('adjacent', list())
        reset = kwargs.get('reset', False)
        val = int(not reset)
        for color in adjacent:
            if move.color >= color:
                self.used[move.color - 1][color - 1] = val
            else:
                self.used[color - 1][move.color - 1] = val
        self.move_index += 1

    def back(self, move: CrateMove, **kwargs):
        adj = kwargs.get('adjacent', list())
        self.move(move, adjacent=adj, reset=True)
        self.move_index -= 1

    def check_move(self, move: int, adjacent: List[int]) -> bool:
        for color in adjacent:
            if move >= color and self.used[move - 1][color - 1] == 1:
                return False
            elif self.used[color - 1][move - 1] == 1:
                return False
        return True

    def filter_moves(self, moves: List[CrateMove], **kwargs) -> List[Move]:
        adjacent: List[int] = kwargs.get('adjacent', list())
        return [move for move in moves if self.check_move(move.color, adjacent) and move.color not in adjacent]


class Crate(Problem):
    def __init__(self, size: int):
        self.size = size
        self.colors = 2 * size
        self.crate = numpy.zeros((size, size), dtype="int_")
        if size % 2 is not 0:
            self.colors += 1
        self.state = CrateState(self.colors, [CrateMove((0, 0))])

    def __str__(self):
        return str(self.crate) + "\n"

    def is_done(self):
        return 0 not in self.crate

    def adjacent_pos(self, pos: Tuple[int, int]):
        (x, y) = pos
        out = (-1, self.size)
        return [(x, y) for x, y in [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)] if
                x not in out and y not in out]

    def adjacent_colors(self, pos: Tuple[int, int]):
        result = [self.crate[(x, y)] for x, y in self.adjacent_pos(pos) if self.crate[(x, y)] != 0]
        return result

    def get_next(self, pos: CrateMove) -> List[Move]:
        (x, y) = pos.position
        return [CrateMove((x, y)) for x, y in self.adjacent_pos((x, y))
                if self.crate[(x, y)] == 0
                and not self.state.in_next((x, y))]

    def get_moves(self, move: CrateMove) -> List[Move]:
        all_moves = [CrateMove(move.position, color) for color in range(1, self.colors + 1)]
        return self.state.filter_moves(all_moves, adjacent=self.adjacent_colors(move.position))

    def move(self, move: CrateMove):
        self.crate[move.position] = move.color
        self.state.move(move, adjacent=self.adjacent_colors(move.position))

    def back(self, move):
        self.crate[move.position] = 0
        self.state.back(move, adjacent=self.adjacent_colors(move.position))

    def get_state(self):
        return self.state


class CSP:
    def __init__(self, problem: Problem):
        self.problem = problem
        self.state = problem.get_state()

    def solve(self):
        print(problem)
        if self.problem.is_done():
            return True
        result = False
        pos = self.state.get_next_move()
        self.state.add_next(self.problem.get_next(pos))
        possible = self.problem.get_moves(pos)
        for move in possible:
            self.problem.move(move)
            result = self.solve()
            if result:
                break
        if not result:
            self.problem.back(pos)
        return result


problem = Crate(5)
csp = CSP(problem)
csp.solve()
print(0 in problem.crate)