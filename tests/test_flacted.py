from __future__ import annotations

from typing import TYPE_CHECKING

from flacted.cli import flacted_main

if TYPE_CHECKING:
    from pathlib import Path

    from click.testing import CliRunner
    from pytest_mock import MockerFixture
    import pytest


def test_flacted_main_show_tag(
    mocker: MockerFixture, runner: CliRunner, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    f = tmp_path / 'file.flac'
    f.write_text('dummy')
    monkeypatch.setattr('sys.argv', ['flac-title', str(f)])
    mocker.patch('flacted.cli.sp.run', return_value=mocker.MagicMock(stdout='TITLE=Test\n'))
    result = runner.invoke(flacted_main, [str(f)])
    assert result.exit_code == 0


def test_flacted_main_show_tag_year(
    mocker: MockerFixture, runner: CliRunner, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    f = tmp_path / 'file.flac'
    f.write_text('dummy')
    monkeypatch.setattr('sys.argv', ['flac-year', str(f)])
    mocker.patch('flacted.cli.sp.run', return_value=mocker.MagicMock(stdout='DATE=Test\n'))
    result = runner.invoke(flacted_main, [str(f)])
    assert result.exit_code == 0


def test_flacted_main_show_tag_track(
    mocker: MockerFixture, runner: CliRunner, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    f = tmp_path / 'file.flac'
    f.write_text('dummy')
    f2 = tmp_path / 'file2.flac'
    f2.write_text('dummy')
    monkeypatch.setattr('sys.argv', ['flac-track', str(f), str(f2)])
    mocker.patch('flacted.cli.sp.run', return_value=mocker.MagicMock(stdout='TRACK=1\n'))
    result = runner.invoke(flacted_main, [str(f), str(f2)])
    assert f'{f}: 01' in result.output
    assert f'{f2}: 01' in result.output
    assert result.exit_code == 0


def test_flacted_main_show_tag_track_invalid_value_for_int(
    mocker: MockerFixture, runner: CliRunner, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    f = tmp_path / 'file.flac'
    f.write_text('dummy')
    monkeypatch.setattr('sys.argv', ['flac-track', str(f)])
    mocker.patch('flacted.cli.sp.run', return_value=mocker.MagicMock(stdout='TRACK=a\n'))
    result = runner.invoke(flacted_main, [str(f)])
    assert result.exit_code == 0
    assert not result.output.strip()


def test_flacted_main_show_tag_track_invalid_metaflac_output(
    mocker: MockerFixture, runner: CliRunner, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    f = tmp_path / 'file.flac'
    f.write_text('dummy')
    monkeypatch.setattr('sys.argv', ['flac-track', str(f)])
    mocker.patch('flacted.cli.sp.run', return_value=mocker.MagicMock(stdout='\n'))
    result = runner.invoke(flacted_main, [str(f)])
    assert result.exit_code == 0
    assert not result.output.strip()


def test_flacted_main_set_tags(
    mocker: MockerFixture, runner: CliRunner, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    f = tmp_path / 'file.flac'
    f.write_text('dummy')
    mocker.patch('flacted.cli.sp.run', return_value=mocker.MagicMock(stdout=''))
    args = (
        str(f),
        '--album',
        'A',
        '--artist',
        'B',
        '-D',
        '-y',
        '2023',
        '-T',
        '1',
        '-p',
        'image.jpg',
    )
    monkeypatch.setattr('sys.argv', ['flacted', *args])
    result = runner.invoke(flacted_main, args)
    assert result.exit_code == 0


def test_flacted_main_set_tags_no_destroy(
    mocker: MockerFixture, runner: CliRunner, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    f = tmp_path / 'file.flac'
    f.write_text('dummy')
    mocker.patch('flacted.cli.sp.run', return_value=mocker.MagicMock(stdout=''))
    args = (str(f), '--album', 'A', '--artist', 'B', '-y', '2023', '-T', '1', '-p', 'image.jpg')
    monkeypatch.setattr('sys.argv', ['flacted', *args])
    result = runner.invoke(flacted_main, args)
    assert result.exit_code == 0


def test_flacted_main_no_args(runner: CliRunner) -> None:
    result = runner.invoke(flacted_main, [])
    assert result.exit_code != 0
