local utils = import 'utils.libjsonnet';

{
  uses_user_defaults: true,
  description: 'Front-end to metaflac to set common FLAC tags.',
  keywords: ['flac', 'metaflac', 'tagging'],
  project_name: 'flacted',
  version: '0.0.2',
  want_main: true,
  want_flatpak: true,
  publishing+: { flathub: 'sh.tat.flacted' },
  want_man: true,
  has_multiple_entry_points: true,
  pyproject+: {
    project+: {
      scripts: {
        'flac-album': 'flacted.cli:flacted_main',
        'flac-artist': 'flacted.cli:flacted_main',
        'flac-genre': 'flacted.cli:flacted_main',
        'flac-title': 'flacted.cli:flacted_main',
        'flac-track': 'flacted.cli:flacted_main',
        'flac-year': 'flacted.cli:flacted_main',
        flacted: 'flacted.cli:flacted_main',
      },
    },
    tool+: {
      poetry+: {
        dependencies+: {
          deltona: utils.latestPypiPackageVersionCaret('deltona'),
        },
      },
    },
  },
  pyinstaller+: {
    include_only: ['flacted'],
  },
  appimage+: {
    include_only: ['flacted'],
  },
}
