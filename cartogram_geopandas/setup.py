# -*- coding: utf-8 -*-
"""
cartogram_geopandas
"""

from setuptools import setup
from Cython.Build import cythonize

setup(
    name='cartogram_geopandas',
    version='0.0.0c',
    description='Fast and convenient cartogram creation on a GeoDataFrame',
    author='mthh',
    install_requires = ['cython','shapely==1.8.5.post1'],
    py_modules=['cartogram_geopandas'],
    ext_modules=cythonize("cycartogram.pyx", language_level="3"),
    license='GPL v2',
    )
