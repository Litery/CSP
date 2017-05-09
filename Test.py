import time
from CrateHC import Crate
from CSP import CSP
import tabulate as tb


def test1(traverse, insight, scope):
    def current_milli_time(): return int(round(time.time() * 1000))
    cols = ['Size', 'BT_time', 'FC_time', 'BT_iters', 'FC_iters']
    row_format = "{:>15}" * 5
    print(row_format.format(*cols))
    for i in range(*scope):
        data = []
        init = (int(i / 2), int(i / 2))
        data.append(i)
        problem1 = Crate(i, init)
        problem2 = Crate(i, init)
        csp1 = CSP(problem1)
        timer = current_milli_time()
        csp1.back_tracking(traverse=traverse)
        timer = current_milli_time() - timer
        data.append(timer)
        csp2 = CSP(problem2)
        timer = current_milli_time()
        csp2.forward_checking(max_insight=insight, traverse=traverse)
        timer = current_milli_time() - timer
        data.append(timer)
        data.append(csp1.visits)
        data.append(csp2.visits)
        print(row_format.format(*data))


def test2():
    problem = Crate(3)
    csp = CSP(problem)
    csp.back_tracking(log=True)


test1(1, 12, (2, 11))
