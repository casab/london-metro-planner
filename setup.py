# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

setup(
    name='london_metro',
    version='0.1.0',
    description='P',
    author='owners',
    author_email='me@test.com',
    packages=find_packages(exclude=('tests', 'docs'))
)