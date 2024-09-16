from setuptools import setup, find_packages

setup(
    name='lite-py-di',
    version='0.1',
    packages=find_packages(where='lite-py-di'),
    package_dir={'': 'lite-py-di'},
    install_requires=[],
    author='VortexOsxo',
    description='A Simple dependency injection module for python',
    url='https://github.com/VortexOsxo/py-dependency-injection-module',
)