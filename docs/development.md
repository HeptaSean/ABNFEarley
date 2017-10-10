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

For this, you need to have [pip](https://pip.pypa.io/en/stable/) installed
(and, since we are developing for Python 3 exclusively, it should be the
version for Python 3).
Install it with the package manager of your operating system, e.g., by
`sudo apt install python3-pip` on Ubuntu and other Debian-based
distributions or by `sudo pacman -S python-pip` on Arch Linux.

Now, we need _virtualenv_ and _virtualenvwrapper_:
```sh
sudo -H pip3 install virtualenv virtualenvwrapper
```

We add the following at the end of _.bashrc_:
```sh
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export WORKON_HOME=~/PythonEnvs
source /usr/local/bin/virtualenvwrapper.sh
```
The path to _virtualenvwrapper.sh_ might be different on your system.

We create a virtual environment for the _abnfearley_ project, which we can
deactivate and later reenter with the helpers from virtualenvwrapper:
```sh
mkvirtualenv abnfearley
deactivate
workon abnfearley
```

## Setup Development Installation with _pip_
Since we have a separate _src_ folder, we cannot import the modules in the
_abnfearley_ package without doing a development installation.
From within our development virtual environment do:
```sh
pip install -e /path/to/ABNFEarley
```

This does an editable install of our package in the _site-packages_ of the
virtual environment and, hence, makes the modules in our package available
independently of the current working directory.

## Run Tests with _unittest_
TODO: First tests and documentation
