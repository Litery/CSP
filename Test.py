import time
from CrateHC import Crate
from CSP import CSP


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
        csp2.forward_checking(max_insight=i, traverse=traverse)
        timer = current_milli_time() - timer
        data.append(timer)
        data.append(csp1.visits)
        data.append(csp2.visits)
        print(row_format.format(*data))


def test2(size):
    init = (int(size / 2), int(size / 2))
    problem = Crate(size)
    csp = CSP(problem)
    csp.back_tracking(log=True)

def test3(size):
    init = (int(size / 2), int(size / 2))
    problem = Crate(size, init)
    csp = CSP(problem)
    csp.forward_checking(10, log=True)


test1(2, 12, (2, 9))
# test3(5)