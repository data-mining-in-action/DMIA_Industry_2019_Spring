import numpy as np

def func1():
    np.random.seed(42)
    values = []
    for _ in range(10000):
        values.append((np.random.randint(0, 2, size=10000) * 2 - 1).mean())  
    return np.array(values)


def func2():
    np.random.seed(42)
    return (np.random.randint(0, 2, size=(10000, 10000)) * 2 - 1).mean(axis=1)


def func3():
    np.random.seed(42)
    values = []
    for _ in range(10):
        values.extend((np.random.randint(0, 2, size=(1000, 10000)) * 2 - 1).mean(axis=1))
    return np.array(values)


def func4():
    np.random.seed(42)
    values = []
    for _ in range(100):
        values.extend((np.random.randint(0, 2, size=(100, 10000)) * 2 - 1).mean(axis=1))
    return np.array(values)


def func5():
    np.random.seed(42)
    values = []
    for _ in range(1000):
        values.extend((np.random.randint(0, 2, size=(10, 10000)) * 2 - 1).mean(axis=1))
    return np.array(values)
