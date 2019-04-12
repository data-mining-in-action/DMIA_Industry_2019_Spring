from setuptools import setup, find_packages

setup(
    name='ml_pure',
    install_requires=['numpy'],
    packages=find_packages(include=('ml_pure*',))
)
