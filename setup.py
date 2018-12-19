from setuptools import setup, find_packages

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

    packages=find_packages(),

    url='https://github.com/SelfHacked/util',
    author='SelfHacked',
)
