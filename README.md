# AVR-VMC-PeripheralControl-Module

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Build PeripheralControl Module](https://github.com/bellflight/AVR-VMC-PeripheralControl-Module/actions/workflows/build.yml/badge.svg)](https://github.com/bellflight/AVR-VMC-PeripheralControl-Module/actions/workflows/build.yml)

The Peripheral Control module is responsible for communicating with the PCC over
serial. This is a thin MQTT to serial bridge.

## Development

It's assumed you have a version of Python installed from
[python.org](https://python.org) that is the same or newer as
defined in the [`Dockerfile`](Dockerfile).

First, install [Poetry](https://python-poetry.org/):

```bash
python -m pip install pipx --upgrade
pipx ensurepath
pipx install poetry
# (Optionally) Add pre-commit plugin
poetry self add poetry-pre-commit-plugin
```

Now, you can clone the repo and install dependencies:

```bash
git clone https://github.com/bellflight/AVR-VMC-PeripheralControl-Module
cd AVR-VMC-PeripheralControl-Module
poetry install --sync
poetry run pre-commit install --install-hooks
```

Run

```bash
poetry shell
```

to activate the virtual environment.
