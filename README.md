# aiida-archive [IN-DEVELOPMENT]

This repository contains a package for prototyping a new archive format.

- `aiida_archive/interface.py` provides an abstract base class for the backend API interface
- `aiida_archive/backends` provides different backends to implements this interface.
- Each backend is also assigned to an entry-point in the `aiida.archive_format` group.
- `aiida_archive/cli.py` implements a simple CLI interface to the API.

This package utilises [flit](https://flit.readthedocs.io) as the build engine, and [tox](https://tox.readthedocs.io) for test automation.

To list all the development environments:

```
pip install tox
tox -a -v
```

To try out the CLI:

```
tox -e py37-cli -- --help
```

To run the pytest suite:

```
tox -e py37
```

To check type annotations:

```
tox -e py37-mypy
```

To run the pre-commit style formatting and linting:

```
pip install pre-commit
pre-commit run --all
```
