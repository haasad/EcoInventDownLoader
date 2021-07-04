from setuptools import setup

setup(
    name='eidl',
    packages=['eidl'],
    version='1.3.0',
    author="Adrian Haas",
    url="https://github.com/haasad/EcoInventDownLoader",
    license=open('LICENSE').read(),
    description='Download, unpack and import ecoinvent into your brightway2 project in one simple step',
    long_description=open('README.md').read()
)
