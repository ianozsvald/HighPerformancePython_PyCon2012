from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

# python setup_cython.py build_ext --inplace

import numpy

ext = Extension("calculate_z", ["calculate_z.pyx"],
    include_dirs = [numpy.get_include()],
    # adding openmp arguments for openmp variant (not required normally)
    extra_compile_args=['-fopenmp'],
    extra_link_args=['-fopenmp']
    )

# note that the compile and link flags with -fopenmp and *only* required for
# the prange variant, they aren't required for the range(...) version and
# could be removed

setup(ext_modules=[ext],
      cmdclass = {'build_ext': build_ext})

