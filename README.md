# aiida-archive [IN-DEVELOPMENT]

This repository contains a package for prototyping a new archive format, to inform <https://github.com/aiidateam/AEP/pull/21>.

- `aiida_archive/interface.py` provides an abstract base class for the backend API interface
- `aiida_archive/backends` provides different backends to implements this interface.
- Each backend is also assigned to an entry-point in the `aiida.archive_format` group.
- `aiida_archive/cli.py` implements a simple CLI interface to the API.

This package utilises [flit](https://flit.readthedocs.io) as the build engine, and [tox](https://tox.readthedocs.io) for test automation.

To list all the development environments:

```console
$ pip install tox
$ tox -a -v
```

To try out the CLI:

```console
$ tox -e py37-cli -- --help
py37-cli run-test: commands[0] | aiida-archive --help
Usage: aiida-archive [OPTIONS] COMMAND [ARGS]...

  The command line interface for aiida-archive

Options:
  -v, --version       Show the version and exit.
  --list-backends     Print the available backend plugins and exit
  -b, --backend TEXT  The entry point of the backend.  [default: current]
  -p, --path FILE     Path to the archive file.  [default: aiida.archive]
  -h, --help          Show this message and exit.

Commands:
  count     Print the number of nodes.
  versions  Print the archive version information.

```

To run the pytest suite:

```console
$ tox -e py37
```

To check type annotations:

```console
$ tox -e py37-mypy
```

To run the pre-commit style formatting and linting:

```console
$ pip install pre-commit
$ pre-commit run --all
```
