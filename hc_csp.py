import random
import numpy
import matplotlib.pyplot as plt
import time



class Crate:
    def __init__(self, size):
        self.size = size
        self.colors = 2 * size
        self.crate = numpy.zeros((size, size), dtype="int_")
        if size % 2 is not 0:
            self.colors += 1

    def load_active1(self, x, y):
        out = (-1, self.size)
        return [(x, y) for x, y in [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)] if
                x not in out and y not in out and self.crate[(x, y)] == 0]

    def get_colors1(self, x, y, used):
        out = (-1, len(self.crate))
        adjacent = [(x, y) for x, y in [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)] if
                    x not in out and y not in out and self.crate[(x, y)] != 0]
        adj_col = [self.crate[(x, y)] for x, y in adjacent]
        return [col for col in range(1, 1 + self.colors) if
                col not in adj_col and set() == {(col, adj) for adj in adj_col} & used], adj_col, adjacent

    def color1(self, used, active):
        if 0 not in self.crate:
            return True, None
        x, y = active[0]
        result = None
        colors, adj_colors, adjacent = self.get_colors1(x, y, used)
        # self.log(used, active, colors)
        random.shuffle(colors)
        for color in colors:
            self.crate[(x, y)] = color
            new_used = {(color, adj) for adj in adj_colors} | {(adj, color) for adj in adj_colors}
            new_active = active[1:] + [(a, b) for a, b in self.load_active1(x, y) if (a, b) not in active]
            result, faulty = self.color1(used | new_used, new_active)
            if result is True:
                break
                # elif active[0] not in faulty:
                #     adjacent = faulty
                #     break
        if not result:
            self.crate[(x, y)] = 0
        return result, adjacent

    def log(self, used, active, colors, color=None):
        print("Active nodes: " + str(active))
        print("Possible colors: " + str(colors))
        print("Current color: " + str(color))
        print("Used combinations: " + str({(x, y) for (x, y) in used}))
        print("Used combinations wt color: " + str({(x, y) for (x, y) in used if x == color or y == color}))
        numpy.set_printoptions(precision=0, formatter={'int': lambda x: '{:02}'.format(x) if x != 0 else "--"})
        for row in self.crate:
            print(row)
        input()


def to_image(crate, colors):
    size = numpy.ceil(numpy.power(colors, 1 / 3))
    # imgplot = plt.imshow(crate/colors, cmap="hsv")
    im = plt.imshow(crate, cmap="hsv", animated=True)
    plt.pause(0.00001)


# crt = Crate(4)
# fig = plt.figure()
# ims = []
# animation = ani.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=1000)
# x, y = crt.color1(numpy.zeros((4, 4), dtype="int_"), set(), [(2, 2)])
# plt.show()
# print(x)
# to_image(numpy.zeros((6, 6)), 16)

current_milli_time = lambda: int(round(time.time() * 1000))


def test1():
    for size in range(1, 12):
        crt = Crate(size)
        timer = current_milli_time()
        x, y = crt.color1(set(), [(int(size / 2), int(size / 2))])
        timer = current_milli_time() - timer
        print("size: " + str(size) + " time: " + str(timer))
        print(crt.crate)


def test2():
    crt = Crate(5)
    x, y = crt.color1(set(), [(2, 2)])
    print(x)
    print(y)


x = [1, 2, 3]
y = x + [5]
print(x)
