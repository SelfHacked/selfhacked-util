# SelfHacked Util

## Developing this project

* Setting up:

        pip install -e .[test]

* Testing:

    Local testing:

        pytest

    Push your own branch and tests will run on [Travis](https://travis-ci.com/).

* Test Coverage

        pytest --cov

## Using this project

* Development version:

        pip install -e .

* GitHub version:

    In `requirements.txt`

        git+git://github.com/SelfHacked/selfhacked-util.git

    The branch is `master` by default.
    To specify a branch,

        git+git://github.com/SelfHacked/selfhacked-util.git@{branch}
