
from setuptools import setup, find_packages
from os import path

setup(
	name='schemello',
	version='.2',
	description='A tool for building advanced text formatting functions.',
    url='https://github.com/knathanwilson/schemello',
    author='Nathaniel Wilson',
    author_email='knathanwilson@gmail.com',
    packages=find_packages(),
    python_requires='>=2.7',
)
