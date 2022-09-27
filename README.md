# Workspace Service

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg?style=for-the-badge)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.9](https://img.shields.io/badge/python-3.9-brightgreen?style=for-the-badge)](https://www.python.org/)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/pilotdataplatform/workspace/ci/main?style=for-the-badge)](https://github.com/PilotDataPlatform/workspace/actions/workflows/cicd.yml)
[![codecov](https://img.shields.io/codecov/c/github/PilotDataPlatform/workspace?style=for-the-badge)](https://codecov.io/gh/PilotDataPlatform/workspace)

Provides APIs to help manage workspace resources such as Guacamole.

## Getting Started

### Prerequisites

This project is using [Poetry](https://python-poetry.org/docs/#installation) to handle the dependencies. Installtion instruction for poetry can be found at https://python-poetry.org/docs/#installation

### Installation & Quick Start

1. Clone the project.

       git clone https://github.com/PilotDataPlatform/workspace.git

2. Install dependencies.

       poetry install

3. Add environment variables into `.env`. Use `.env.schema` as a reference.

4. Run application.

       poetry run python start.py

### Startup using Docker

This project can also be started using [Docker](https://www.docker.com/get-started/).

1. To build and start the service within the Docker container, run:

       docker compose up


## Resources

* [Pilot Platform API Documentation](https://pilotdataplatform.github.io/api-docs/)
* [Pilot Platform Helm Charts](https://github.com/PilotDataPlatform/helm-charts/)

## Contribution

You can contribute the project in following ways:

* Report a bug.
* Suggest a feature.
* Open a pull request for fixing issues or adding functionality. Please consider
  using [pre-commit](https://pre-commit.com) in this case.

