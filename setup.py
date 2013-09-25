import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="turtlepower",
    version="0.1",
    author="Simon Davy",
    author_email="bloodearnest@gmail.com",
    description=("A tool for advanced use of the turtle module"),
    license="MIT",
    keywords="turtle education kids",
    url="https://github.com/AllTheWayDown/turtlepower",
    packages=find_packages(),
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Education",
        "Topic :: Games/Entertainment :: Simulation",
    ],
)
