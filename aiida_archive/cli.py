"""A CLI for the archive."""
import sys
from typing import Any, List, Union

import click

from aiida_archive.interface import AiidaArchive

if sys.version_info >= (3, 8):
    from importlib import metadata as importlib_metadata
else:
    import importlib_metadata

ENTRY_GROUP = "aiida.archive_format"


def _load_plugin(name: str) -> AiidaArchive:
    for entry_point in importlib_metadata.entry_points().get(ENTRY_GROUP, ()):
        if entry_point.name == name:
            return entry_point.load()
    raise ImportError(f"{ENTRY_GROUP}:{name} entry point not found")


def _list_plugins() -> List[str]:
    return [ep.name for ep in importlib_metadata.entry_points().get(ENTRY_GROUP, ())]


def callback_list_backends(
    ctx: click.Context, param: Union[click.Option, click.Parameter], value: Any
) -> Any:
    if not value or ctx.resilient_parsing:
        return
    click.echo("\n".join(_list_plugins()))
    ctx.exit()


pass_archive = click.make_pass_decorator(AiidaArchive)


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(None, "-v", "--version")
@click.option(
    "--list-backends",
    is_flag=True,
    expose_value=False,
    is_eager=True,
    callback=callback_list_backends,
    help="Print the available backend plugins and exit",
)
@click.option(
    "-b",
    "--backend",
    default="current",
    show_default=True,
    help="The entry point of the backend.",
    type=str,
)
@click.option(
    "-p",
    "--path",
    default="aiida.archive",
    show_default=True,
    help="Path to the archive file.",
    type=click.Path(exists=False, dir_okay=False),
)
@click.pass_context
def main(ctx: click.Context, backend: str, path: str) -> None:
    """The command line interface for aiida-archive """
    # TODO mypy complains: "AiidaArchive" not callable
    ctx.obj = _load_plugin(backend)(path)  # type: ignore


@main.command("versions")
@pass_archive
def versions(archive: AiidaArchive) -> None:
    """Print the archive version information."""
    archive_version = archive.get_version_archive()
    aiida_version = archive.get_version_aiida()
    click.echo(f"Archive: {archive_version}\nAiiDA:   {aiida_version}")


@main.command("count")
@pass_archive
def count(archive: AiidaArchive) -> None:
    """Print the number of nodes."""
    click.echo(str(len(list(archive.iter_uuids_nodes()))))
