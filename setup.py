import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="CHANGEME",
    version="0.0.0",
    author="Andrew Sledge",
    author_email="andrew.j.sledge@gmail.com",
    description=("CHANGE ME"),
    license="BSD",
    keywords="keyword keyword",
    url="CHANGEME",
    packages=['CHANGEME', 'CHANGEME'],
    long_description=read('README.md'),
    classifiers=[
        #"Development Status :: 3 - Alpha",
        #"Topic :: Utilities",
        #"License :: OSI Approved :: BSD License",
    ],
)
