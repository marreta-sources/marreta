#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
from os.path import dirname, join
from setuptools import setup, find_packages

# requirements
with open('requirements.txt') as f:
    required = f.read().splitlines()

with open(join(dirname(__file__), 'marreta/VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name="marreta",
    version=version,
    description="Marreta dual custody password system",
    long_description=open('README.rst').read(),
    author="Marreco",
    author_email="coder@marreco.org",
    maintainer="Bruno Costa, Kairo Araujo",
    maintainer_email="coder@marreco.org",
    url="https://github.com/marreco/marreta/",
    keywords="Marreta, dual, custody, password, system",
    packages=find_packages(exclude=['*.test', 'tests.*']),
    install_requires=required,
    include_package_data=True,
    license='Apache Software License',
    platforms='Posix; MacOS X; Windows',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Unix',
        'Topic :: Security',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
