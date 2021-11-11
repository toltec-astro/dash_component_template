#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['anytree', 'numpy', 'dash', 'dash_bootstrap_components']

test_requirements = ['pytest>=3', ]

setup(
    author="Zhiyuan Ma",
    author_email='zhiyuanma@umass.edu',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    description="A framework to create reusable Dash layout.",
    install_requires=requirements,
    license="BSD license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='dash_component_template',
    name='dash_component_template',
    packages=find_packages(
        include=['dash_component_template', 'dash_component_template.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/toltec-astro/dash_component_template',
    version='0.1.0',
    zip_safe=False,
)
