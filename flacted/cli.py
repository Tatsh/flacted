"""CLI for flacted."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, cast
import logging
import subprocess as sp
import sys

if TYPE_CHECKING:
    from collections.abc import Callable

from bascom import setup_logging
from deltona.constants import CONTEXT_SETTINGS
import click

log = logging.getLogger(__name__)

__all__ = ('flacted_main',)


def _show_tag_values(
    metaflac: Callable[..., sp.CompletedProcess[str]],
    files: tuple[Path, ...],
    tag_requested: str,
) -> None:
    possible: tuple[str, ...] = (tag_requested.title(), tag_requested.upper(), tag_requested)
    if tag_requested == 'year':
        possible += ('Date', 'DATE', 'date')
    show_filename = len(files) > 1
    for filename in files:
        for tag in possible:
            val = metaflac(f'--show-tag={tag}', filename).stdout.strip()
            try:
                val = val[len(tag) + 1 :].splitlines()[0].strip()
            except IndexError:
                val = ''
            if not val:
                continue
            if tag_requested == 'track':
                try:
                    val_int: int | None = int(val)
                except (TypeError, ValueError):
                    val = ''
                    val_int = None
                if val_int is not None:
                    val = f'{val_int:02d}'
            if show_filename:
                click.echo(f'{filename}: {val}')
            else:
                click.echo(val)
            break


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('files', nargs=-1, type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option('-A', '--album', help='Album.')
@click.option(
    '-D', '--delete-all-before', is_flag=True, help='Delete all existing tags before processing.'
)
@click.option('-T', '--track', type=int, help='Track number.')
@click.option('-a', '--artist', help='Track artist.')
@click.option('-d', '--debug', is_flag=True, help='Enable debug output.')
@click.option('-g', '--genre', help='Genre.')
@click.option('-p', '--picture', help='Cover artwork to attach.')
@click.option('-t', '--title', help='Track title.')
@click.option('-y', '--year', type=int, help='Year.')
def flacted_main(
    files: tuple[Path, ...],
    album: str | None = None,
    artist: str | None = None,
    genre: str | None = None,
    picture: str | None = None,
    title: str | None = None,
    track: int | None = None,
    year: int | None = None,
    *,
    debug: bool = False,
    delete_all_before: bool = False,
) -> None:
    """Front-end to metaflac to set common tags."""  # noqa: DOC501
    setup_logging(debug=debug, loggers={'flacted': {}})

    def metaflac(*args: Any, **kwargs: Any) -> sp.CompletedProcess[str]:
        return sp.run(
            ('metaflac', *cast('tuple[str, ...]', args)),
            capture_output=not debug,
            **kwargs,
            check=True,
            text=True,
        )

    invoked_as = Path(sys.argv[0]).name
    if invoked_as != 'flacted' and len(files) > 0:
        tag_requested = invoked_as.split('-')[1].lower()
        _show_tag_values(metaflac, files, tag_requested)
        return
    min_args = 3
    metaflac_args = ['--preserve-modtime', '--no-utf8-convert']
    clean_up_args = metaflac_args.copy()
    destroy = delete_all_before
    clean_up_args.append('--remove-all-tags')
    clean_up_args += (str(x) for x in files)
    for key, value in {
        'album': album,
        'artist': artist,
        'genre': genre,
        'title': title,
        'track': track,
        'year': year,
    }.items():
        if not value:
            continue
        value_ = value.strip() if isinstance(value, str) else value
        match key:
            case 'year':
                flac_tag = 'Date'
            case 'track':
                flac_tag = 'Tracknumber'
            case _:
                flac_tag = f'{key[0].upper()}{key[1:]}'
        metaflac_args.append(f'--set-tag={flac_tag}={value_}')
    if picture:
        metaflac_args.append(f'--import-picture-from={picture}')
    if len(metaflac_args) < min_args:
        click.echo('Not doing anything.', err=True)
        raise click.Abort
    if destroy:
        metaflac(*clean_up_args)
    metaflac_args += (str(x) for x in files)
    metaflac(*metaflac_args)
