local utils = import 'utils.libjsonnet';

{
  description: 'Front-end to metaflac to set common FLAC tags.',
  keywords: ['flac', 'metaflac', 'tagging'],
  project_name: 'flacted',
  version: '0.0.0',
  want_main: true,
  want_man: true,
  supported_python_versions: ['3.12', '3.13'],
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
          deltona: {
            python: '>=3.12,<3.14',
            version: utils.latestPypiPackageVersionCaret('deltona'),
          },
        },
      },
    },
  },
  copilot: {
    intro: 'flacted is a front-end to metaflac to set common FLAC tags.',
  },
}
