from typing import Any, Iterable, List, Optional

from packaging.version import Version

from aiida import load_profile
from aiida.common.folders import SandboxFolder
from aiida.orm import load_node
from aiida.tools.importexport import Archive, import_data

from aiida_archive.interface import AiidaArchive

from .export import export


class NonRepoArchive(Archive):
    """An archive that does unpack into the repo.

    Unpacking into the repo requires one actually exists,
    which should not be necessary for archive inspection.
    """

    def __enter__(self) -> "NonRepoArchive":
        """Instantiate a SandboxFolder into which the archive can be lazily unpacked."""
        self._folder = SandboxFolder(sandbox_in_repo=False)
        return self


class CurrentArchive(AiidaArchive):
    """The current archive implementation."""

    def get_version_archive(self) -> Version:
        with NonRepoArchive(str(self.location)) as archive_object:
            version = archive_object.version_format
        return Version(version)

    def get_version_aiida(self) -> Version:
        with NonRepoArchive(str(self.location)) as archive_object:
            version = archive_object.version_aiida
        return Version(version)

    def iter_uuids_nodes(self) -> Iterable[str]:
        """Return an iterator of uuids."""
        with NonRepoArchive(str(self.location)) as archive_object:
            data = archive_object.data
        for node in data["export_data"]["Node"].values():
            yield node["uuid"]

    def push(
        self, uuids: List[str], *, profile: Optional[str] = None, **kwargs: Any
    ) -> None:
        """Export nodes to an archive.

        :param uuids: the list of node UUIDs to push to the archive.
        :param profile: The AiiDA profile name (or use default)

        """
        load_profile(profile)
        export([load_node(uid) for uid in uuids], filename=str(self.location))

    def pull(self, *, profile: Optional[str] = None, **kwargs: Any) -> None:
        """Import nodes from an archive.

        :param profile: The AiiDA profile name (or use default)

        """
        if "uuids" in kwargs:
            raise NotImplementedError("Cannot specify particular UUIDs")
        load_profile(profile)
        import_data(str(self.location))
