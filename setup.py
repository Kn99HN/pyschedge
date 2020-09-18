import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name='pyschedge',
    version='0.0.1',
    description='A light weight Python wrapper for the Schedge API',
    long_description=README,
    long_description_content_type="text/markdown",
    author="@Kn99HN",
    author_email="khanhnguyen99hn@gmail.com",
    url='https://github.com/Kn99HN/pyschedge',
    install_requires=['requests'],
    license='MIT',
    packages=['pyschedge'])