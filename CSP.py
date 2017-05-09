import random
from Abstracts import Problem


class CSP:
    def __init__(self, problem: Problem):
        self.problem = problem
        self.visits = 0

    def back_tracking(self, log=False, traverse=0):
        return self.forward_checking(0, log, traverse)

    def forward_checking(self, max_insight, log=False, traverse=0):
        self.visits += 1
        log = log
        traverse = traverse
        problem = self.problem
        if problem.is_done():
            return True
        result = False
        node = problem.get_next_node()
        possible = problem.get_moves(node)
        if traverse is 1:
            possible.sort(key=lambda move: problem.rate_move(move))
        elif traverse is 2:
            random.shuffle(possible)
        elif traverse is 3 and self.visits % 2 == 0:
            possible.reverse()
        for move in possible:
            problem.load_next_nodes(node)
            problem.move(move, node)
            forward_check = problem.have_moves(max_insight)
            if log:
                print('Node:' + str(node))
                print('Possible:' + str(possible))
                fcheck = [(problem.get_moves(node), node) for node in problem.get_next_nodes(max_insight)]
                print('Forward check:' + str(fcheck))
                self.problem.print()
                input()
            if forward_check:
                result = self.forward_checking(max_insight, log, traverse)
            if result:
                break
            problem.back(move, node)
        return result

