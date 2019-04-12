from setuptools import setup, find_packages

setup(
    name='ml_numba',
    install_requires=['numpy', 'numba'],
    packages=find_packages(include=('ml_numba*',))
)
