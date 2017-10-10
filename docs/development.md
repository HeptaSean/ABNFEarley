# Development Environment

## Cloning the Repository
If you want to modify the code, you can clone this repository with git:
```sh
git clone https://github.com/HeptaSean/ABNFEarley.git
```

If you want your changes included in the upstream code, you can create a
pull request.
You should fork the repository to your own GitHub account and push your
changes to a separate branch there.
The process of creating the pull request is described in the [GitHub
Help](https://help.github.com/articles/creating-a-pull-request-from-a-fork/).
If you started with a direct clone of this repository, you can [add your
fork as additional remote](https://stackoverflow.com/a/11620086), which
also allows you to keep your changes in sync with this upstream repository.

## Installing virtualenv
As a Python developer, you should work in a [virtual
environment](https://virtualenv.pypa.io/en/stable/).

For this, you need to have [`pip`](https://pip.pypa.io/en/stable/)
installed (and, since we are developing for Python 3 exclusively, it should
be the version for Python 3).
Install it with the package manager of your operating system, e.g., by
`sudo apt install python3-pip` on Ubuntu and other Debian-based
distributions or by `sudo pacman -S python-pip` on Arch Linux.

Now, we need `virtualenv` and `virtualenvwrapper`:
```sh
sudo -H pip3 install virtualenv virtualenvwrapper
```

We add the following at the end of `.bashrc`:
```sh
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export WORKON_HOME=~/PythonEnvs
source /usr/local/bin/virtualenvwrapper.sh
```
The path to `virtualenvwrapper.sh` might be different on your system.

We create a virtual environment for the _ABNFEarley_ project, which we can
deactivate and later reenter with the helpers from `virtualenvwrapper`:
```sh
mkvirtualenv abnfearley
deactivate
workon abnfearley
```

## Setup Development Installation with `pip`
Since we have a separate `src` folder, we cannot import the modules in the
`abnfearley` package from our main folder without doing a development
installation.
From within our development virtual environment do:
```sh
pip install -e /path/to/ABNFEarley
```

This does an editable install of our package in the `site-packages` of the
virtual environment and, hence, makes the modules in our package available
independently of the current working directory.

## Tests with `unittest` and `doctest`
TODO: First tests and documentation

## Development Cycle
We try to adhere to a development strategy, where we repeat the following
steps:
1. We draft the documentation of a feature (more or less complete).
2. We write unit tests according to the documentation.
3. We implement the feature and test it with the unit tests.
4. We clarify the documentation and add (`doctest`able) examples.

Bug fixes and small enhancements can often skip steps 1 and 4 if they are
to small or exceptional to be referred to in the documentation.

If you want to report an issue, it is of great help to include a unit test
showing the problem, perhaps even in an issue branch in a forked
repositiory, so that the issue test and hopefully also its solution can
later easily be integrated by a pull request.
