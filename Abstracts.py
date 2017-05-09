from abc import ABC, abstractmethod
from typing import List, Iterable, TypeVar

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
    def get_moves(self, node: Node) ->List[Move]:
        pass

    @abstractmethod
    def have_moves(self, depth: int) -> bool:
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
