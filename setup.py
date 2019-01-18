from setuptools import setup, find_packages

setup(
    name='selfhacked-util',

    version='dev',

    python_requires='>=3.6',

    install_requires=[
        'Django>=1.11',
    ],

    extras_require={
        'test': [
            'pytest',
            'pytest-runner',
            'pytest-dependency @ https://github.com/SelfHacked/pytest-dependency/archive/master.zip',
        ],
    },

    packages=find_packages(),
    include_package_data=True,

    url='https://github.com/SelfHacked/util',
    author='SelfHacked',
)
