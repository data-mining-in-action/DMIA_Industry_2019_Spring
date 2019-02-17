import numpy
import scipy

from seminar1_project.extra_module import help_function


def cool_function(x):
    """
    very cool function
    :param x: number
    :return: x + 42
    """
    print('cool_function')
    return x + 42


def cool_function_plus_one(x):
    print('cool_function_plus_one')
    help_function()
    return cool_function(x + 1)


if __name__ == '__main__':
    print(numpy.__version__)
    print(scipy.__version__)
    print(cool_function_plus_one(0))
