#!/usr/bin/env python

from setuptools import setup

from arcadiamock import __VERSION__


setup(name='arcadiamock',
      version=__VERSION__,
      description='Mock the ARCADIA REST services',
      author='Franck Chauvel',
      author_email='franck.chauvel@sintef.no',
      url='https://github.com/SINTEF-9012/arcadia-mock',
      packages=["arcadiamock"],
      test_suite="tests",
      entry_points = {
          'console_scripts': [
              'arcadiamock = arcadiamock.server:main'
          ]
      }
     )
