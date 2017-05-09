import random
from typing import Tuple, List
from Abstracts import Problem

class Queens(Problem):
    def __init__(self):
        pass

    def get_next_nodes(self, length: int):
        return super().get_next_nodes(length)

    def print(self) -> None:
        pass

    def back(self, move: int, node: Tuple[int, int]):
        pass

    def has_moves(self, node: Tuple[int, int]) -> bool:
        pass

    def get_moves(self, node: Tuple[int, int]) -> List[int]:
        pass

    def load_next_nodes(self, node) -> None:
        pass

    def rate_move(self, move: int):
        pass

    def move(self, move: int, node: Tuple[int, int]):
        pass

    def get_next_node(self) -> Tuple[int, int]:
        pass

    def is_done(self) -> bool:
        pass