"""Are You Still There is a simple Python library testing if
email addresses actually exist.

"""
from setuptools import setup

setup(
    name='areyoustillthere',
    version='0.1.0',
    long_description=__doc__,
    packages=['ayst'],
    include_package_data=True,
    author='Anthony Grimes',
    author_email='i@raynes.me',
    url='https://github.com/Raynes/areyoustillthere',
    description='Find dem emails yo.',
    license='MIT',
    install_requires=['pydns>=2.3.6']
)
