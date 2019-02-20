from setuptools import setup, find_packages

extra_django = [
    'Django>=1.11',
]
extra_aws = [
    'boto3>=1.9',
    'botocore',
]
extra_all = extra_django + extra_aws

extra_test = [
    'pytest>=4',
    'pytest-runner>=4',
    'pytest-dependency @ https://github.com/SelfHacked/pytest-dependency/archive/master.zip',
]
extra_dev = extra_all + extra_test

setup(
    name='selfhacked-util',

    version='dev',

    python_requires='>=3.6',

    extras_require={
        'django': extra_django,
        'aws': extra_aws,

        'all': extra_all,

        'test': extra_test,
        'dev': extra_dev,
    },

    packages=find_packages(),
    include_package_data=True,

    url='https://github.com/SelfHacked/selfhacked-util',
    author='SelfHacked',
)
