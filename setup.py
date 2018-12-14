from setuptools import setup

setup(
    name='selfhacked-util',

    version='dev',

    python_requires='>=3.6',

    install_requires=[
        'Django>=1.11',
    ],

    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],

    packages=['selfhacked'],

    url='https://github.com/SelfHacked/util',
    author='SelfHacked',
)
