# ChangeLog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.13](https://github.com/wesky93/grpc_requests/releases/tag/v0.1.13) - 2023-12-03

## Added

- Added channel interceptors for standard and async clients

## Fixed

- Refactored how methods and services are added to description pool to better avoid cases where FileDescriptors may be added twice.

## [0.1.12](https://github.com/wesky93/grpc_requests/releases/tag/v0.1.12) - 2023-11-26

## Added

- Method to print out a generic descriptor added to utils collection
- Helper methods to print out a method's request and responses in a human readable format

## Changed

- Documentation revamped
- Version checks to avoid using deprecated methods added to async client

## Fixed

- Include `requirements.txt` in build manifest

## Deprecated

- Method to retrieve fields for the descriptor of a method's input type.

## Added

## [0.1.11](https://github.com/wesky93/grpc_requests/releases/tag/v0.1.11) - 2023-10-05

## Added

- Method to retrieve fields for the descriptor of a method's input type.

## Changes

- Updates to minimum versons of requirements to address vulnerabilities

## [0.1.10](https://github.com/wesky93/grpc_requests/releases/tag/v0.1.10) - 2023-03-07

## Fixed

- Corrected pin of `protobuf` version in `requirements.txt`

## [0.1.9](https://github.com/wesky93/grpc_requests/releases/tag/v0.1.9) - 2023-02-14

### Changes

- Reimplementation of test case framework
- Restoration of reflection client test cases
- Updates to continuous integration pipeline

## [0.1.8](https://github.com/wesky93/grpc_requests/releases/tag/v0.1.8) - 2023-01-24

### Changes

- Update project and dev dependencies to versions that require Python >= 3.7
- Update project documentation and examples

## [0.1.7](https://github.com/wesky93/grpc_requests/releases/tag/v0.1.7) - 2022-12-16

### Deprecated

- homi dependency, as the project has been archived
- homi dependent test code

## [0.1.6](https://github.com/spaceone-dev/grpc_requests/releases/tag/v0.1.6) - 2022-11-10

### Fixed

- Ignore repeat imports of protobufs and reflecting against a server

## [0.1.3](https://github.com/spaceone-dev/grpc_requests/releases/tag/v0.1.3) - 2022-7-14

### Fixed

- remove click

### Issues

- ignore test before deploy

## [0.1.2](https://github.com/spaceone-dev/grpc_requests/releases/tag/v0.1.2) - 2022-7-7

## [0.1.1](https://github.com/spaceone-dev/grpc_requests/releases/tag/v0.1.1) - 2022-6-13

### Changes

- remove unused package : click #35

## [0.1.0](https://github.com/spaceone-dev/grpc_requests/releases/tag/v0.1.0) - 2021-8-21

### Added

- Full TLS connection support

### Fixed

- Ignore reflection if service already registered

### Changed

- Update grpcio version

## [0.0.10](https://github.com/spaceone-dev/grpc_requests/releases/tag/v0.0.10) - 2021-2-27

### Fixed

- Fix 3.6 compatibility issue : await is in f-string

## [0.0.9](https://github.com/spaceone-dev/grpc_requests/releases/tag/v0.0.9) - 2020-12-25

### Added

- Support AsyncIO API

## [0.0.8](https://github.com/spaceone-dev/grpc_requests/releases/tag/0.0.8) - 2020-11-24

### Added

- Add StubClient

### Fixed

- Bypasss kwargs to base client

## [0.0.7](https://github.com/spaceone-dev/grpc_requests/releases/tag/v0.0.7) - 2020-10-4

### Added

- Support Compression

## [0.0.6](https://github.com/spaceone-dev/grpc_requests/releases/tag/v0.0.6) - 2020-10-3

### Added

- Support TLS connections

## [0.0.5](https://github.com/spaceone-dev/grpc_requests/releases/tag/v0.0.5) - 2020-9-9

### Changed

- Response filled gets original proto field name rather than(before returned lowerCamelCase)

## [0.0.4](https://github.com/spaceone-dev/grpc_requests/releases/tag/v0.0.4) - 2020-7-21

## [0.0.3](https://github.com/spaceone-dev/grpc_requests/releases/tag/v0.0.3) - 2020-7-21

### Added

- Dynamic request method
- Service client

## [0.0.2](https://github.com/spaceone-dev/grpc_requests/releases/tag/v0.0.2) - 2020-7-20

### Added

- Support all method types
- Add request test case

## [0.0.1](https://github.com/spaceone-dev/grpc_requests/releases/tag/v0.0.1) - 2020-7-20

### Added

- Sync proto using reflection
- Auto convert request(response) from(to) dict
- Support unary-unary
