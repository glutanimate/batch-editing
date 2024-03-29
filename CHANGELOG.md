# Changelog

All notable changes to Batch Editing will be documented here. You can click on each release number to be directed to a detailed log of all code commits for that particular release. The download links will direct you to the GitHub release page, allowing you to manually install a release if you want.

If you enjoy Batch Editing, please consider supporting my work on Patreon, or by buying me a cup of coffee :coffee::

<p align="center">
<a href="https://www.patreon.com/glutanimate" rel="nofollow" title="Support me on Patreon 😄"><img src="https://glutanimate.com/logos/patreon_button.svg"></a>      <a href="https://ko-fi.com/X8X0L4YV" rel="nofollow" title="Buy me a coffee 😊"><img src="https://glutanimate.com/logos/kofi_button.svg"></a>
</p>

:heart: My heartfelt thanks goes out to everyone who has supported this add-on through their tips, contributions, or any other means (you know who you are!). All of this would not have been possible without you. Thank you for being awesome!

## [Unreleased]

## [0.4.0] - 2023-10-26

### [Download](https://github.com/glutanimate/batch-editing/releases/tag/v0.4.0)

### Added

- Added support for Anki 23.10 (thanks to @khonkhortisan for the report)

### Fixed

- Fixed image button icon not working (thanks to @dollajas for the report)
- Fixed image format changing from PNG to JPG when pasting images (thanks to @AH349 for the report)

### Changed

- Modernized and rewrote large parts of the codebase
- Fixed deprecated use of `note.model` (thanks to @Arthur-Milchior, #17)

## [0.3.0] - 2019-06-02

### [Download](https://github.com/glutanimate/batch-editing/releases/tag/v0.3.0)

**Important note for Anki 2.0 users**: As this release completely overhauls the add-on structure, you will have to uninstall any existing versions of the add-on before updating. Otherwise you might end up with duplicate versions of the add-on that would interfere with each other. This should not be an issue on Anki 2.1

### Fixed

- 2.1: Fixed attaching images from the clipboard (#5, thanks to donfed for the report)
- 2.1: Fixed image icon (#5, thanks to reynie78 for the report)
- 2.1: Pre-emptive fix for anki.lang errors

### Changed

- Renamed add-on to "Batch Editing"
- Refactored add-on to improve stability and maintainability

## 0.2.0 - 2017-08-23

### Added

- Anki 2.1 compatibility

## 0.1.3 - 2017-08-06

### Added

- Ability to insert text as HTML

## 0.1.2 - 2017-05-13

### Fixed

- Only insert line-breaks when necessary

## 0.1.1 - 2016-12-11

### Added

- Support for adding text before existing content (thanks to @luminousspice for the idea)

## 0.1.0 - 2016-12-08

### Added

- Initial release of Batch Editing

[Unreleased]: https://github.com/glutanimate/batch-editing/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/glutanimate/batch-editing/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/glutanimate/batch-editing/releases/tag/v0.3.0

-----

The format of this file is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).