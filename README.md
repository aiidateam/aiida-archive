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

## Results

```bash
tox -- tests/test_nodes.py
```

```python
BENCH_RECORDS = 1e5
BENCH_ROUNDS_WRITE = 5
BENCH_ROUNDS_QUERY = 1000
```

pytest-benchmark:

```
------------------------------------------------------------------------------------------------------- benchmark: 6 tests ------------------------------------------------------------------------------------------------------
Name (time in us)                   Min                       Max                      Mean                  StdDev                    Median                     IQR            Outliers       OPS            Rounds  Iterations
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_query_jsonlines           636.4690 (1.0)        919,816.3220 (210.53)     183,378.8216 (75.38)    113,467.1693 (326.40)     183,872.5275 (78.78)    191,539.7520 (493.83)      419;1    5.4532 (0.01)       1000           1
test_query_sqlite            2,003.7720 (3.15)         4,369.0590 (1.0)          2,432.8641 (1.0)          347.6350 (1.0)          2,333.8945 (1.0)          387.8675 (1.0)        250;43  411.0382 (1.0)        1000           1
test_query_json             70,530.1740 (110.81)      86,329.1790 (19.76)       73,883.7807 (30.37)      2,729.4798 (7.85)        72,914.4930 (31.24)      2,440.2765 (6.29)       155;85   13.5348 (0.03)       1000           1
test_write_jsonlines       421,693.1110 (662.55)     431,053.0130 (98.66)      425,057.2058 (174.71)     3,683.6830 (10.60)      424,875.4290 (182.05)     4,455.2170 (11.49)         1;0    2.3526 (0.01)          5           1
test_write_json            459,596.8650 (722.10)     469,781.7390 (107.52)     464,576.7192 (190.96)     3,774.4738 (10.86)      463,766.9170 (198.71)     4,737.6442 (12.21)         2;0    2.1525 (0.01)          5           1
test_write_sqlite        8,231,700.5540 (>1000.0)  8,697,492.9620 (>1000.0)  8,431,712.6916 (>1000.0)  224,972.5055 (647.15)   8,346,871.9930 (>1000.0)  424,636.3807 (>1000.0)       1;0    0.1186 (0.00)          5           1
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

pytest-monitor:

```json
[
  {
    "SESSION_H": "0b8515dd2c6c8b4106429678687001b1",
    "ENV_H": "f844ceca6735add80b94b9fed59f0ed6",
    "ITEM_START_TIME": "2020-10-13T13:53:36.345073",
    "ITEM_PATH": "test_nodes",
    "ITEM": "test_write_json",
    "ITEM_VARIANT": "test_write_json",
    "ITEM_FS_LOC": "tests/test_nodes.py",
    "KIND": "function",
    "COMPONENT": "",
    "TOTAL_TIME": 2.5054640769958496,
    "USER_TIME": 2.287546624,
    "KERNEL_TIME": 0.17593593600000001,
    "CPU_USAGE": 0.9832440155972274,
    "MEM_USAGE": 81.13671875
  },
  {
    "SESSION_H": "0b8515dd2c6c8b4106429678687001b1",
    "ENV_H": "f844ceca6735add80b94b9fed59f0ed6",
    "ITEM_START_TIME": "2020-10-13T13:53:38.858367",
    "ITEM_PATH": "test_nodes",
    "ITEM": "test_write_jsonlines",
    "ITEM_VARIANT": "test_write_jsonlines",
    "ITEM_FS_LOC": "tests/test_nodes.py",
    "KIND": "function",
    "COMPONENT": "",
    "TOTAL_TIME": 2.3041951656341553,
    "USER_TIME": 2.1789977599999997,
    "KERNEL_TIME": 0.10383635200000008,
    "CPU_USAGE": 0.9907294946397144,
    "MEM_USAGE": 45.49609375
  },
  {
    "SESSION_H": "0b8515dd2c6c8b4106429678687001b1",
    "ENV_H": "f844ceca6735add80b94b9fed59f0ed6",
    "ITEM_START_TIME": "2020-10-13T13:53:41.168918",
    "ITEM_PATH": "test_nodes",
    "ITEM": "test_write_sqlite",
    "ITEM_VARIANT": "test_write_sqlite",
    "ITEM_FS_LOC": "tests/test_nodes.py",
    "KIND": "function",
    "COMPONENT": "",
    "TOTAL_TIME": 43.03916001319885,
    "USER_TIME": 41.757581312,
    "KERNEL_TIME": 1.062521984,
    "CPU_USAGE": 0.99491029292552,
    "MEM_USAGE": 280.2578125
  },
  {
    "SESSION_H": "0b8515dd2c6c8b4106429678687001b1",
    "ENV_H": "f844ceca6735add80b94b9fed59f0ed6",
    "ITEM_START_TIME": "2020-10-13T13:54:24.213988",
    "ITEM_PATH": "test_nodes",
    "ITEM": "test_query_json",
    "ITEM_VARIANT": "test_query_json",
    "ITEM_FS_LOC": "tests/test_nodes.py",
    "KIND": "function",
    "COMPONENT": "",
    "TOTAL_TIME": 8.875702857971191,
    "USER_TIME": 7.144058880000003,
    "KERNEL_TIME": 1.531923456,
    "CPU_USAGE": 0.977498061261501,
    "MEM_USAGE": 103.8515625
  },
  {
    "SESSION_H": "0b8515dd2c6c8b4106429678687001b1",
    "ENV_H": "f844ceca6735add80b94b9fed59f0ed6",
    "ITEM_START_TIME": "2020-10-13T13:54:33.096788",
    "ITEM_PATH": "test_nodes",
    "ITEM": "test_query_jsonlines",
    "ITEM_VARIANT": "test_query_jsonlines",
    "ITEM_FS_LOC": "tests/test_nodes.py",
    "KIND": "function",
    "COMPONENT": "",
    "TOTAL_TIME": 17.912132024765015,
    "USER_TIME": 17.608306687999992,
    "KERNEL_TIME": 0.20144460800000008,
    "CPU_USAGE": 0.9942842801390994,
    "MEM_USAGE": 73.984375
  },
  {
    "SESSION_H": "0b8515dd2c6c8b4106429678687001b1",
    "ENV_H": "f844ceca6735add80b94b9fed59f0ed6",
    "ITEM_START_TIME": "2020-10-13T13:54:51.015623",
    "ITEM_PATH": "test_nodes",
    "ITEM": "test_query_sqlite",
    "ITEM_VARIANT": "test_query_sqlite",
    "ITEM_FS_LOC": "tests/test_nodes.py",
    "KIND": "function",
    "COMPONENT": "",
    "TOTAL_TIME": 8.883131265640259,
    "USER_TIME": 8.530403328000006,
    "KERNEL_TIME": 0.2870208000000005,
    "CPU_USAGE": 0.9926031558382564,
    "MEM_USAGE": 271.26953125
  }
]
```
