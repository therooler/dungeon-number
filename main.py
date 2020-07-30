import numpy as np
import matplotlib.pyplot as plt
import copy
from typing import List

PRECISION = 10


def a_sub_b(a: float, b: float) -> float:
    """
    Use Python's magic to express numbers in decimal bases

    :param a: number
    :param b: base
    :return: new number
    """
    number_int = str(int(a))
    number_dec = str(a - int(a)).split('.')[1][:PRECISION]
    num = 0
    for i, dig in enumerate(number_int + number_dec):
        num += int(dig) * (b ** (len(number_int) - i - 1))
    return num


def metallic_mean(n: int) -> float:
    """
    Express the metallic mean for n=1,...,N

    :param n:
    :return:
    """
    return (n + np.sqrt(n ** 2 + 4)) / 2


def decimal_staircase(number: float, dungeon_depth: int)->List[float]:
    """
    Calculate a dungeon number staircase of depth D according to https://www.youtube.com/watch?v=HFeKdMf01rQ 
    
    :param number: number and base of the dungeon number. They are set equal for out purposes.
    :param dungeon_depth: depth of the dungeon (very informative)
    :return: List of all numbers in the dungeon
    """
    base = copy.copy(number)
    numbers = []
    for _ in range(dungeon_depth):
        base = a_sub_b(number, base)
        numbers.append(base)
    return numbers


if __name__ == "__main__":
    """Plot the starting point a versus the final dungeon value phi"""
    golden_ratio = decimal_staircase(1.1, 100)
    print("The golden ratio from a dungeon starting at 1.1 is {}".format(golden_ratio))

    line = None
    fig, axs = plt.subplots(1, 1)
    # take steps of 0.1
    grid = np.array([1 + x * 0.1 for x in range(90)])
    endpoints = []
    # use the data in line for potenial fractal plots.
    for a in grid:
        line = decimal_staircase(a, 100)
        line.insert(0, a)
        endpoints.append(line[-1])
    endpoints = np.array(endpoints)
    cmap = plt.get_cmap('BuPu')

    # plot the endpoints
    axs.plot(grid, endpoints, '.', color=cmap(0.5))
     # plot the metallic means
    for n in range(1, 10):
        axs.plot(grid, [metallic_mean(n)] * len(grid), label='metallic ratio n = {}'.format(n),
                 color=cmap(float(n) / 10), linestyle='--')
        idx = np.isclose(endpoints, metallic_mean(n), atol=0.01)
        if len(idx):
            axs.plot(grid[idx], endpoints[idx], color=cmap(float(n + 2) / 10), markersize=20, marker='x')
    axs.legend()
    axs.set_ylabel('$\phi$')
    axs.set_xlabel('$a$')
    plt.show()
