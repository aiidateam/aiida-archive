from packaging.version import Version
import pytest

from aiida_archive.backends.current import CurrentArchive


def test_get_version_archive(data_path):
    archive = CurrentArchive(data_path / "current.graph1.aiida")
    assert archive.get_version_archive() == Version("0.9")


def test_get_version_aiida(data_path):
    archive = CurrentArchive(data_path / "current.graph1.aiida")
    assert archive.get_version_aiida() == Version("1.4.1")


def test_iter_uuids_nodes(data_path):
    archive = CurrentArchive(data_path / "current.graph1.aiida")
    assert sorted(archive.iter_uuids_nodes()) == [
        "0a8223e7-fc7f-490f-8c99-962c1e3e17af",
        "0ea79a16-501f-408a-8c84-a2704a778e4b",
        "33c97bcd-dc91-4a25-9874-11e519cb5a8e",
        "387faed6-46a8-4a3c-a998-f60cd097086a",
        "4ac72b6c-ce4c-4cb2-8053-9164c8f81437",
        "6b413465-37b0-4064-ac52-65f560b42194",
        "779636a5-bc18-4c76-8f8c-2c54bcb4868c",
        "79e2417a-5aa5-4787-bd7c-74152cd8a729",
        "b23e692e-4e01-48dd-b515-4c63877d73a4",
        "beeeb810-c694-4fee-aeca-d49a233b832b",
    ]


@pytest.mark.usefixtures("clear_database_before_test")
def test_push(tmp_path, provenance_tree):
    archive = CurrentArchive(tmp_path / "aiida.archive")
    node = provenance_tree()
    archive.push([node.uuid])


@pytest.mark.usefixtures("clear_database_before_test")
def test_pull(data_path):
    archive = CurrentArchive(data_path / "current.graph1.aiida")
    archive.pull()
