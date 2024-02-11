#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import unittest
import re
from os.path import join, dirname, abspath


SETUP_DIR = dirname(abspath(__file__))
PROJECT_URL = 'https://github.com/thomasvolk/fretty'
PROJECT_FILES_URL = 'https://raw.githubusercontent.com/thomasvolk/fretty'

with open(join(SETUP_DIR, 'fretty', '__init__.py')) as f:
    VERSION = re.search("__version__\s=\s'(.*)'", f.read()).group(1)


def project_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='*_test.py')
    return test_suite


with open('README.md') as f:
    long_description = f.read()
    long_description = long_description.replace('<img src="example/', f'<img src="{PROJECT_FILES_URL}/master/example/')


setup(
    name='fretty',
    description='Fretty is a guitar fretboard generator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=VERSION,
    include_package_data=True,
    author="Thomas Volk",
    author_email="info@thomasvolk.de",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Markup"
    ],
    packages=find_packages(exclude=("tests",)),
    entry_points = {
        'console_scripts': ['fretty=fretty:main'],
    },
    extras_require={
        "PNG": ["CairoSVG"],
    },
    url=PROJECT_URL,
    license='Apache',
    platforms='any',
    python_requires='>=3.9.0'
)