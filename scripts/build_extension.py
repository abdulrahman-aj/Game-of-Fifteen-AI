# python3 setup.py build
from distutils.core import setup, Extension

module = Extension("fifteen_solver", sources=["./lib/fifteen_solver.cpp", "./lib/util.cpp"])

setup(
    name="fifteen_solver",
    version="1.0",
    description="15/8 Puzzle Solver",
    ext_modules=[module])
