# SelfHacked Util

## Developing this project

* Setting up:

        pip install -e .

* Testing:

    Local testing:

        python setup.py test

    Push your own branch and tests will run on [Travis](https://travis-ci.com/).

## Using this project

* Development version:

        pip install -e .

* GitHub version:

    In `requirements.txt`

        git+git://github.com/SelfHacked/util.git

    The branch is `master` by default.
    To specify a branch,

        git+git://github.com/SelfHacked/util.git@{branch}
