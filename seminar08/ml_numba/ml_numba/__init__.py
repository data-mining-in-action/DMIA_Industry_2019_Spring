from numba import jit, prange
import numpy as np


@jit(nopython=True)
def func1():
    np.random.seed(42)
    values = []
    for i in range(10000):
        values.append((np.random.randint(0, 2, size=10000) * 2 - 1).mean())  
    return np.array(values)

@jit(nopython=True)
def func2():
    np.random.seed(42)
    values = []
    for i in range(10000):
        res = 0
        for j in range(10000):
            res += np.random.randint(0, 2) * 2 - 1
        values.append(res / 10000)
    return np.array(values)
