#!/usr/bin/env python

from distutils.core import setup

from arcadiamock import __VERSION__

setup(name='arcadiamock',
      version=__VERSION__,
      description='MOCK the ARCADIA REST services',
      author='Franck Chauvel',
      author_email='franck.chauvel@sintef.no',
      url='',
      packages=["arcadiamock"],
      entry_points = {
          'console_scripts': [
              'arcadiamock = arcadiamock.server:main'
          ]
      }
     )
