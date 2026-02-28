"""Sphinx configuration."""

from __future__ import annotations

from datetime import UTC, datetime
from operator import itemgetter
from pathlib import Path
import sys

import tomlkit

with (Path(__file__).parent.parent / 'pyproject.toml').open(newline='\n', encoding='utf-8') as f:
    project_ = tomlkit.load(f).unwrap()['project']
    authors_list, name, version = itemgetter('authors', 'name', 'version')(project_)
authors = [f'{d["name"]} <{d["email"]}>' for d in authors_list]
sys.path.insert(0, str(Path(__file__).parent.parent))
author = f'{authors_list[0]["name"]} <{authors_list[0]["email"]}>'
copyright = str(datetime.now(UTC).year)  # noqa: A001
project = name
release = f'v{version}'
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx', 'sphinx.ext.napoleon', 'sphinx_click']
html_theme = 'alabaster'
intersphinx_mapping = {
    'click': ('https://click.palletsprojects.com/en/latest/', None),
    'python': ('https://docs.python.org/3', None),
}
