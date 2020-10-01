"""Configuration file for pytest tests."""
from io import StringIO
from pathlib import Path
from typing import Optional

import pytest

from aiida.common.links import LinkType
from aiida.engine import ProcessState
from aiida.orm import CalcFunctionNode, Data, Dict

pytest_plugins = ["aiida.manage.tests.pytest_fixtures"]


@pytest.fixture()
def data_path():
    """Path to data folder"""
    return Path(__file__).parent / "data"


@pytest.fixture()
def provenance_tree():
    """Recursively build a test provenance tree."""

    def _generate(
        *,
        root: Optional[Data] = None,
        depth: int = 1,
        breadth: int = 1,
        objects: int = 0
    ) -> Data:
        """Recursively build a test provenance tree.

        :param root: The root node to use, otherwise one is created.
        :param depth: The depth of the provenance tree
        :param breadth: The breadth of the provenance tree
        :param objects: The number of objects to store on each data node

        :returns: The root node
        """
        if root is None:
            root = Data()
        if not root.is_stored:
            root.store()
        if depth < 1:
            return
        depth -= 1
        for _ in range(breadth):
            calcfunc = CalcFunctionNode()
            calcfunc.set_process_state(ProcessState.FINISHED)
            calcfunc.set_exit_status(0)
            calcfunc.add_incoming(
                root, link_type=LinkType.INPUT_CALC, link_label="input"
            )
            calcfunc.store()

            out_node = Dict(dict={str(i): i for i in range(10)})
            for idx in range(objects):
                out_node.put_object_from_filelike(
                    StringIO("a" * 10000), "key" + str(idx)
                )
            out_node.add_incoming(
                calcfunc, link_type=LinkType.CREATE, link_label="output"
            )
            out_node.store()

            calcfunc.seal()

            _generate(root=out_node, depth=depth, breadth=breadth, objects=objects)

        return root

    return _generate
