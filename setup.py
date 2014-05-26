from setuptools import setup

setup(
    name='areyoustillthere',
    version='1.0',
    long_description=__doc__,
    packages=['areyoustillthere'],
    include_package_data=True,
    author='Anthony Grimes',
    description='Find dem emails yo.',
    license='MIT',
    install_requires=['requests>=2.2.1', 'nameparser>=0.2.9',
                      'pydns>=2.3.6', 'gevent>=1.0.1',
                      'rapportive'],
)
