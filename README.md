# SelfHacked Util

[![Build Status](https://travis-ci.com/SelfHacked/selfhacked-util.svg?branch=master)](https://travis-ci.com/SelfHacked/selfhacked-util)
[![Coverage Status](https://coveralls.io/repos/github/SelfHacked/selfhacked-util/badge.svg?branch=master)](https://coveralls.io/github/SelfHacked/selfhacked-util?branch=master)

Note: Some files are not included in coverage.
See [`.coveragerc`](.coveragerc) for details.

## Developing this project

* Setting up:

    ```bash
    pip install -e .[dev]
    ```

* Testing:

    Local testing:

    ```bash
    pytest
    ```

    Push your own branch and tests will run on [Travis](https://travis-ci.com/).

* Test Coverage

    ```bash
    pytest --cov
    ```

    To see lines not covered in tests,

    ```bash
    pytest --cov --cov-report term-missing
    ```

## Using this project

* Development version:

    ```bash
    pip install -e .
    ```

* GitHub version:

    ```bash
    pip install git+git://github.com/SelfHacked/selfhacked-util.git#egg=selfhacked-util
    ```

    Installs from the `master` branch by default.
    To specify a branch/tag/commit,

    ```bash
    pip install git+git://github.com/SelfHacked/selfhacked-util.git@{ref}#egg=selfhacked-util
    ```

* Installing extras

    There are three extra options (see `extras_require` in `setup.py`):
    `aws`, `django` and `all`.
    To install an extra, simply add `[xxx]` at the end (no space).
