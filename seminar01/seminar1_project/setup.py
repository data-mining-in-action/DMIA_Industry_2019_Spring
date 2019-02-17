import os
from setuptools import find_packages, setup


included_packages = ('seminar1_project*',)
setup_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(setup_dir, 'requirements.txt'), 'r') as req_file:
    requirements = [line.strip() for line in req_file if line.strip()]

setup(
    name='seminar1_project',
    version='1.0.0',
    zip_safe=False,
    install_requires=requirements,
    packages=find_packages(include=included_packages)
)
