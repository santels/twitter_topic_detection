from distutils.core import setup
from distutils.extension import Extension

import numpy

USE_CYTHON = True
SRC = 'src/'

cmdclass = {}
ext = '.pyx' if USE_CYTHON else '.c'


ext_modules = [
                Extension("src.calculate_similarity",
                        [SRC + "calculate_similarity" + ext],
                        include_dirs=[numpy.get_include()])
              ]

if USE_CYTHON:
    from Cython.Build import cythonize
    from Cython.Distutils import build_ext
    ext_modules = cythonize(ext_modules)
    cmdclass.update({ 'build_ext' : build_ext })

setup(
    name='twitter_topic_detection',
    ext_modules=ext_modules,
    cmdclass=cmdclass,
    author='Andrew Santelices',
    version='1.4'
)
