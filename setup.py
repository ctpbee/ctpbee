from distutils.core import setup
from setuptools import find_packages

pkgs = find_packages()

setup(name='ctpbee',
      version='0.1',
      author='somewheve',
      author_email='somewheve@gmail.com',
      description="easy ctp trade and market support",
      url='https://github.com/somewheve/ctpbee',

      packages=pkgs
      )
