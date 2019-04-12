#from distutils.core import setup
from setuptools import setup
from distutils.extension import Extension

from Cython.Build import cythonize

import numpy

extensions = [Extension(
    "ml_cython", ["src/ml_cython.pyx"],
    include_dirs=[numpy.get_include()]
)]
extensions = cythonize(extensions)

setup(
    name='ml_cython',
    ext_modules = extensions,
    setup_requires=['cython', 'numpy'],
    install_requires=['cython', 'numpy']
)
