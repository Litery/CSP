from abc import ABC, abstractmethod
from typing import List
from typing import NewType


class Move(ABC):
    pass


class State(ABC):
    @abstractmethod
    def add_moves(self):
        pass

    @abstractmethod
    def move(self, move: Move):
        pass


class Problem(ABC):
    @abstractmethod
    def is_done(self):
        pass

    @abstractmethod
    def get_moves(self, moves: List[Move]):
        pass

    @abstractmethod
    def move(self, move: Move):
        pass

    @abstractmethod
    def back(self, move: Move):
        pass
