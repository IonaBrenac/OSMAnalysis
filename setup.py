"""
Setup file
"""

#!/usr/bin/env python

# Standard library imports
from os import path
from pathlib import Path

# 3rd party imports
from setuptools import setup, find_packages

# Setting useful paths
this_directory = path.abspath(path.dirname(__file__))

# Reading the contents of your README file
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    install_requires = f.read().strip().split('\n')

# This setup is suitable for "python setup.py develop".

setup(name='OSMAnalysis',
      version='0.0.0',
      description='An application for open science monitoring',
      long_description=long_description,
      long_description_content_type='text/markdown',
      include_package_data=True,
      license='MIT',
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.13',
        'Topic :: Bibliometry :: Information Analysis :: Visualization',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research'
        ],
      keywords='Bibliometry, BSO, Open science, '
               + 'Research software',
      install_requires=install_requires,
      author='BSO-Analysis team',
      author_email='iona.brenac@protonmail.com, '
                   + 'amal.chabli@orange.fr,',
      url='https://github.com/IonaBrenac/OSMAnalysis',
      packages=find_packages(),
      )
