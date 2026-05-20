# Contributing

This project was built with [Claude Code](https://claude.ai/claude-code). PRs welcome.

## Areas we'd love help with

- **Web UI** -- a browser-based form so users can configure trips without editing YAML. No terminal required. This is the highest-priority community contribution.
- **Additional language voices** -- edge-tts has non-English voices. Extending the pipeline to support Spanish, French, German, and other languages would make this useful for international trips.
- **More interest categories** -- the `config/interests_catalog.yaml` has 51 built-in categories. More are welcome: Dark Sky/astronomy sites, Civil War battlefields, industrial heritage, vineyard routes, literary landmarks, etc.
- **Travel API integrations** -- connecting to open data sources (OpenStreetMap, Wikipedia API, iNaturalist, USGS) to reduce the need for manual research notes in trip configs.
- **Example trip configs** -- contributed `config/examples/` files for different regions (Pacific Coast Highway, Appalachian Trail, Southwest National Parks, Texas Hill Country, etc.).
- **Audio quality improvements** -- SSML support for edge-tts (pauses, emphasis, pronunciation hints), chapter intro music, ambient sound options.
- **Duration presets** -- 30-minute (summary), 45-minute (standard), 90-minute (deep dive) episode length options beyond the current 60-65 minute default.
- **Tests** -- the `src/` pipeline needs pytest coverage, especially for the duration guard and audio stitcher.

## How to contribute

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Submit a pull request with a description of what you built and why

## Code style

Python. No strict linting enforced yet -- just keep it readable. Comments on non-obvious logic are appreciated.

## Questions?

Open a GitHub issue.
