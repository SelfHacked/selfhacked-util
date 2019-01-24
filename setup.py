from setuptools import setup

setup(
    name='selfhacked-util',

    version='dev',

    python_requires='>=3.6',

    extras_require={
        'django': [
            'Django>=1.11',
        ],
    },

    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],

    packages=['selfhacked'],

    url='https://github.com/SelfHacked/selfhacked-util',
    author='SelfHacked',
)
