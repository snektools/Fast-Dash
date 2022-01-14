# coding: utf-8
import os
import sys
from shutil import rmtree
from setuptools import setup, find_packages, Command


DESCRIPTION = 'SNAQL (Templated SQL) with the ability to pull data.'
HERE_PATH = os.path.dirname(os.path.abspath(__file__))
VERSION = '0.1.1'


try:
    with open(os.path.join(HERE_PATH, 'README.md')) as f:
        long_description = '\n' + f.read()
except IOError:
    long_description = DESCRIPTION

setup(
    name='fastdash',
    version=VERSION,
    author='Richard Foley and David Smit (based on the work of Roman Zaiev)',
    author_email='david.d.smit@gmail.com',
    packages=find_packages(),
    license='MIT',
    url='https://github.com/RichFoley/jinjaql',
    description='Transparant *QL usage without ORM',
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=[
        'Jinja2>=2.9.5',
        'schema>=0.6.5',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
