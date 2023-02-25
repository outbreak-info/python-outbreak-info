# ----------------------------------------------------------------------------
# Copyright (c) 2021-, Outbreak.info development team.
#
# Distributed under the terms of the MIT License
#
# The full license is in the file LICENSE.md, distributed with this software.
# ----------------------------------------------------------------------------
from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()


description = ("Python interface to Outbreak.info,"
               " powered by GISAID")


setup(
    name="python-outbreak-info",
    version="1.0",
    packages=find_packages(),
    author="Outbreak.info dev team",
    license='MIT',
    author_email="lhughes@scripps.edu",
    url="https://github.com/outbreak-info/python-outbreak-info",
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=["numpy", "pandas","requests"]
)
