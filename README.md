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
    "SESSION_H": "529d25a6f33b74a8bd47ba8109c20b8d",
    "ENV_H": "6d937dff067c25fb0153d0ba00c8f2a6",
    "ITEM_START_TIME": "2020-10-13T14:06:42.226912",
    "ITEM_PATH": "test_nodes",
    "ITEM": "test_write_json",
    "ITEM_VARIANT": "test_write_json",
    "ITEM_FS_LOC": "tests/test_nodes.py",
    "KIND": "function",
    "COMPONENT": "",
    "TOTAL_TIME": 2.306252956390381,
    "USER_TIME": 2.162450432,
    "KERNEL_TIME": 0.13593900800000003,
    "CPU_USAGE": 0.9965903495674264,
    "MEM_USAGE": 74.80859375
  },
  {
    "SESSION_H": "529d25a6f33b74a8bd47ba8109c20b8d",
    "ENV_H": "6d937dff067c25fb0153d0ba00c8f2a6",
    "ITEM_START_TIME": "2020-10-13T14:06:44.539839",
    "ITEM_PATH": "test_nodes",
    "ITEM": "test_write_jsonlines",
    "ITEM_VARIANT": "test_write_jsonlines",
    "ITEM_FS_LOC": "tests/test_nodes.py",
    "KIND": "function",
    "COMPONENT": "",
    "TOTAL_TIME": 2.124321937561035,
    "USER_TIME": 2.0269957120000006,
    "KERNEL_TIME": 0.07611532799999998,
    "CPU_USAGE": 0.9900152151206484,
    "MEM_USAGE": 44.7109375
  },
  {
    "SESSION_H": "529d25a6f33b74a8bd47ba8109c20b8d",
    "ENV_H": "6d937dff067c25fb0153d0ba00c8f2a6",
    "ITEM_START_TIME": "2020-10-13T14:06:46.671247",
    "ITEM_PATH": "test_nodes",
    "ITEM": "test_write_sqlite",
    "ITEM_VARIANT": "test_write_sqlite",
    "ITEM_FS_LOC": "tests/test_nodes.py",
    "KIND": "function",
    "COMPONENT": "",
    "TOTAL_TIME": 43.96364188194275,
    "USER_TIME": 42.434183680000004,
    "KERNEL_TIME": 1.1372814079999998,
    "CPU_USAGE": 0.9910795198678973,
    "MEM_USAGE": 277
  },
  {
    "SESSION_H": "529d25a6f33b74a8bd47ba8109c20b8d",
    "ENV_H": "6d937dff067c25fb0153d0ba00c8f2a6",
    "ITEM_START_TIME": "2020-10-13T14:07:30.641829",
    "ITEM_PATH": "test_nodes",
    "ITEM": "test_query_json",
    "ITEM_VARIANT": "test_query_json",
    "ITEM_FS_LOC": "tests/test_nodes.py",
    "KIND": "function",
    "COMPONENT": "",
    "TOTAL_TIME": 79.30578804016113,
    "USER_TIME": 64.830574592,
    "KERNEL_TIME": 13.526871168,
    "CPU_USAGE": 0.9880419537640698,
    "MEM_USAGE": 95.8984375
  },
  {
    "SESSION_H": "529d25a6f33b74a8bd47ba8109c20b8d",
    "ENV_H": "6d937dff067c25fb0153d0ba00c8f2a6",
    "ITEM_START_TIME": "2020-10-13T14:08:49.953944",
    "ITEM_PATH": "test_nodes",
    "ITEM": "test_query_jsonlines",
    "ITEM_VARIANT": "test_query_jsonlines",
    "ITEM_FS_LOC": "tests/test_nodes.py",
    "KIND": "function",
    "COMPONENT": "",
    "TOTAL_TIME": 188.64927291870117,
    "USER_TIME": 183.995686912,
    "KERNEL_TIME": 2.110712831999999,
    "CPU_USAGE": 0.9865206309287127,
    "MEM_USAGE": 65.28515625
  },
  {
    "SESSION_H": "529d25a6f33b74a8bd47ba8109c20b8d",
    "ENV_H": "6d937dff067c25fb0153d0ba00c8f2a6",
    "ITEM_START_TIME": "2020-10-13T14:11:58.610007",
    "ITEM_PATH": "test_nodes",
    "ITEM": "test_query_sqlite",
    "ITEM_VARIANT": "test_query_sqlite",
    "ITEM_FS_LOC": "tests/test_nodes.py",
    "KIND": "function",
    "COMPONENT": "",
    "TOTAL_TIME": 12.17725396156311,
    "USER_TIME": 11.210588159999986,
    "KERNEL_TIME": 0.5802393600000002,
    "CPU_USAGE": 0.9682665367099299,
    "MEM_USAGE": 269.86328125
  }
]
```
