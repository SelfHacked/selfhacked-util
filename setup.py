from setuptools import setup, find_packages

extra_django = [
    'Django>=1.11',
]
extra_test = [
    'pytest>=4',
    'pytest-runner>=4',
    'pytest-dependency @ https://github.com/SelfHacked/pytest-dependency/archive/master.zip',
]

setup(
    name='selfhacked-util',

    version='dev',

    python_requires='>=3.6',

    extras_require={
        'django': extra_django,
        'test': extra_test,
    },

    packages=find_packages(),
    include_package_data=True,

    url='https://github.com/SelfHacked/selfhacked-util',
    author='SelfHacked',
)
