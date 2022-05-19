# Release Notes

## [Unreleased](https://github.com/aalcala07/home_dashboard/compare/v0.5.0...0.x)

## [v0.5.0](https://github.com/aalcala07/home_dashboard/compare/v0.4.0...v0.5.0) - 2022-05-19

### Added

- Added ability to enable and configure services from control panel

### Changed

- Made improvements to control panel UI
- Changed how services and locations are stored
- Made control panel enabled by default

### Fixed

- Fixed control panel layouts for mobile

## [v0.4.0](https://github.com/aalcala07/home_dashboard/compare/v0.3.0...v0.4.0) - 2022-05-13

### Added

- Show disk usage on control panel
- Allow changing display configs from control panel and automatically reload web server and display

### Changed

- Renamed web console to control panel
- Activate display using a subprocess

### Fixed

- Fixed uptime and load time averages on control panel


## [v0.3.0](https://github.com/aalcala07/home_dashboard/compare/v0.2.0...v0.3.0) - 2022-05-04

### Changed

- Additional templates must be added to the "templates" folder.

### Added

- Optional web console built with Flask for viewing device and display configurations from the browser
- Device Info component for showing IP address.


## [v0.2.0](https://github.com/aalcala07/home_dashboard/compare/v0.1.0...v0.2.0) - 2022-02-25

### Changed

- Config files for template and services can be set in `.env`
- All components accept `props` as third argument
- Weather and clock components accept location as property
- Weather service can accept multiple locations