"""A generic interface for an archive implementation."""
from abc import ABC, abstractmethod
import os
from pathlib import Path
from typing import Any, Iterable, List, Optional, Union

from packaging.version import Version


class AiidaArchive(ABC):
    def __init__(self, location: Union[str, Path]):
        """Initialise the archive

        :param location: The path of the archive

        """
        self._loc = Path(os.path.abspath(location))

    @property
    def location(self) -> Path:
        return self._loc

    @abstractmethod
    def get_version_archive(self) -> Version:
        """Return the version of the archive."""

    @abstractmethod
    def get_version_aiida(self) -> Version:
        """Return the version of aiida."""

    @abstractmethod
    def iter_uuids_nodes(self) -> Iterable[str]:
        """Return an iterator of node uuids."""

    # TODO handle migrations

    @abstractmethod
    def push(
        self, uuids: List[str], *, profile: Optional[str] = None, **kwargs: Any
    ) -> None:
        """Export nodes to an archive.

        :param uuids: the list of node UUIDs to push to the archive.
        :param profile: The AiiDA profile name (or use default)

        """

    @abstractmethod
    def pull(
        self,
        *,
        profile: Optional[str] = None,
        uuids: Optional[List[str]] = None,
        **kwargs: Any
    ) -> None:
        """Import nodes from an archive.

        :param uuids: the list of node UUIDs to pull from the archive.
            If None, pull all
        :param profile: The AiiDA profile name (or use default)

        """
