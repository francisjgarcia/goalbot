# GoalBot

## Description

GoalBot is a project that aims to provide personalized interactions and motivational messages to users in Twitch streams and Discord forums. The project consists of two interconnected bots: one for Twitch and another for Discord. The primary goal is to provide personalized interactions in Twitch streams based on the goals and objectives shared by users in a Discord forum. Additionally, the bots generate motivational messages for users in both Twitch and Discord using the OpenAI API.

## Key Features

### Discord Bot:

- Retrieves threads from a specific forum channel in Discord.
- Filters messages by author and structures the data of each thread into a JSON format.
- Ignores a specific thread titled "Propósitos 2025" to prevent irrelevant data.
- Provides summaries of forum discussions using OpenAI's API, which generates personalized responses and summaries.

### Twitch Bot:

- Monitors messages in the Twitch chat and reacts when a user has sent enough messages to trigger an automatic response.
- Queries the Discord bot to check if the user has participated in the forums and generates a personalized summary of their goals using the OpenAI API.
- If the user has not shared their goals on Discord, the bot encourages them to participate.
- Sends random motivational messages during the stream while the streamer is live.
- Offers the `!propositos` command, which provides a general summary of all users' goals or the goals of a specific user who has posted on Discord.

### Integration with OpenAI:

- Uses the OpenAI API to generate responses based on Discord forum posts, summarizing and motivating users with personalized messages related to their goals.
- Customizes the bot's interactions based on the user's activity in both Discord and Twitch.

### Streamer Status Monitoring:

- The bot regularly checks whether the streamer is live and adjusts its behavior accordingly, sending automated messages only when the streamer is online.

## How It Works

The Twitch bot tracks the messages sent by users and, after a random number of messages, queries the Discord forum data to see if the user has posted their goals. If they have, the bot generates a personalized motivational message based on their goals. If not, the bot encourages them to participate in Discord. Additionally, the Twitch bot sends random motivational messages at random intervals while the streamer is online.

Both bots run concurrently using a single asyncio event loop, allowing them to interact efficiently with each other while performing their respective tasks.

## Table of Contents

- [GoalBot](#goalbot)
  - [Description](#description)
  - [Key Features](#key-features)
    - [Discord Bot:](#discord-bot)
    - [Twitch Bot:](#twitch-bot)
    - [Integration with OpenAI:](#integration-with-openai)
    - [Streamer Status Monitoring:](#streamer-status-monitoring)
  - [How It Works](#how-it-works)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Prerequisites](#prerequisites)
  - [Usage](#usage)
    - [Cloning the Repository](#cloning-the-repository)
    - [Local Development](#local-development)
    - [Running with Docker](#running-with-docker)
  - [Docker](#docker)
    - [Dockerfile](#dockerfile)
    - [Docker Compose](#docker-compose)
  - [GitHub Actions](#github-actions)
    - [CI/CD Pipeline](#cicd-pipeline)
    - [Deploy to server](#deploy-to-server)
    - [Remove deploy from server](#remove-deploy-from-server)
  - [Secrets Configuration](#secrets-configuration)
  - [Variables Configuration](#variables-configuration)
  - [Documentation](#documentation)
  - [Source Code](#source-code)
  - [Tests](#tests)
---

## Project Structure

```plaintext
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── 0_bug_report.yml                # Template for reporting bugs or issues
│   │   ├── 1_feature_request.yml           # Template for requesting new features
│   │   ├── 2_improvement_request.yml       # Template for suggesting improvements
│   │   ├── 3_performance_issue.yml         # Template for reporting performance issues
│   │   ├── 4_refactor_request.yml          # Template for requesting code refactoring
│   │   ├── 5_documentation_update.yml      # Template for suggesting documentation updates
│   │   ├── 6_security_vulnerability.yml    # Template for reporting security vulnerabilities
│   │   ├── 7_tests_requests.yml            # Template for requesting new tests
│   │   ├── 8_question.yml                  # Template for asking questions
│   │   └── config.yml                      # Configuration file for issue templates
│   ├── workflows/
│   │   ├── cicd.yml                        # CI/CD pipeline configuration using GitHub Actions
│   │   ├── deploy.yml                      # Deploy to server workflow
│   │   └── remove-deploy.yml               # Remove deploy from server workflow
│   ├── dependabot.yml                      # Dependabot configuration for dependency updates
│   └── release.yml                         # Automatic release generation on GitHub
├── docker/
│   ├── .env.example                        # Example environment variables file for Docker
│   ├── Dockerfile                          # Dockerfile to build the project image
│   ├── Dockerfile.local                    # Dockerfile to run the project locally
│   └── compose.yml                         # Docker Compose file to define services and networks
├── docs/
│   ├── VARIABLES.md                        # Documentation about variables needed for integration and deployment
│   ├── SECRETS.md                          # Documentation about secrets needed for deployment
│   └── STYLEGUIDE.md                       # Guidelines for code style and formatting
├── src/
│   ├── .env.example                        # Example environment variables file for the application
│   ├── main.py                             # Main script of the project
│   └── requirements.txt                    # Python dependencies file
├── .dockerignore                           # File to exclude files from Docker context
├── .editorconfig                           # Configuration for code formatting in compatible editors
├── .gitignore                              # File to exclude files and directories from version control
├── AUTHORS                                 # List of authors and contributors to the project
├── CHANGELOG.md (*)                        # History of changes and versions of the project (Created after first main deploy)
├── CODE_OF_CONDUCT.md                      # Code of conduct for project contributors
├── CONTRIBUTING.md                         # Guidelines for contributing to the project
├── GOVERNANCE.md                           # Project governance model and decision-making process
├── LICENSE                                 # Information about the project's license
├── README.md                               # Main documentation of the project
├── SECURITY.md                             # Documentation about project security
└── SUPPORT.md                              # Information on how to get support for the project
```

---

## Prerequisites
Before you begin, make sure you have the following installed in your environment:

- git (obligatory)
- docker (optional, if you want to run the project with Docker)
- docker-compose (optional, if you want to run the project with Docker)
- python (optional, if you want to run the project locally)

## Usage

### Cloning the Repository

To use this template to create a new project, you can clone the repository using the following steps:

1. Click on the "Use this template" button at the top of the repository.
2. Enter the repository name, description, and visibility.
3. Click on the "Create repository from template" button.
4. Clone the newly created repository to your local machine.

```bash
git clone
```

5. Navigate to the cloned repository directory.

```bash
cd <repository-name>
```

6. Start working on your new project!

### Local Development

To develop and test the project locally, follow these steps:

1. Install the dependencies:

```bash
pip install -r src/requirements.txt
```

2. Run the main script:

```bash
python src/main.py
```

### Running with Docker

You can use Docker and Docker Compose to run the project in a container. Ensure Docker and Docker Compose are installed.

1. Navigate to the docker directory, rename the `.env.example` file to `.env`, and adjust the environment variables as needed.

```bash
# Compose environment variables
COMPOSE_PROJECT_NAME=goalbot
COMPOSE_FILE=compose.yml

# General environment variables
PUID=1000
PGID=1000
TZ=Europe/Madrid
```
- **COMPOSE_PROJECT_NAME**: Name of the Docker Compose project.
- **COMPOSE_FILE**: Docker Compose configuration file.
- **PUID**: User ID for the container.
- **PGID**: Group ID for the container.
- **TZ**: Timezone for the container.

1. Build and run the services with Docker Compose:

```bash
compose up -d --build
```
This will build the container image according to the Dockerfile and start the services defined in `compose.yml`.

## Docker

### Dockerfile

The `Dockerfile` in the `docker` directory is used to build the Docker image for the project. The file contains instructions to create the image, including the base image, dependencies, and commands to run the application.

The `Dockerfile.local` is used to run the project locally with Docker. This file is used to build the image and run the container locally.

### Docker Compose

The `compose.yml` file in the `docker` directory defines the services and networks for the project using Docker Compose. This file specifies the container image, environment variables, ports, and volumes needed to run the application.

## GitHub Actions

### CI/CD Pipeline

This repository includes a fully automated CI/CD pipeline using `cicd.yml` GitHub Actions. The pipeline is configured to run on each push to the main or development branches and performs the following tasks:

1. **Setup**: Generates the necessary variables for use in the subsequent tasks.
2. **Build**: Builds the Docker image and saves it locally.
3. **Test**: Runs the tests for the application.
4. **Scan**: Scans the Docker image for vulnerabilities using Trivy.
5. **Push**: Pushes the Docker image to the GitHub Container Registry.
6. **Release**: Automatically generates the changelog and creates a new release on GitHub if deploying to `main`.
7. **Merge**: Merges changes from `main` into the `development` branch if a direct push to `main` occurs.
8. **Deploy**: Deploys the application to remote servers using SSH if deploying to `main`.

### Deploy to server

To deploy an specific version of the application to a remote server. You can use the `deploy.yml` workflow. This workflow is triggered by a manual event. Only the `main` branch and tags are allowed to trigger this workflow.

1. **Setup**: Generates the necessary variables for use in the subsequent tasks.
2. **Deploy**: Deploys the application to remote servers using SSH.

### Remove deploy from server

To remove the application from the remote server, you can use the `remove-deploy.yml` workflow. This workflow is triggered by a manual event. Only the `main` branch is allowed to trigger this workflow.

1. **Setup**: Generates the necessary variables for use in the subsequent tasks.
2. **Remove deploy**: Removes the application from remote servers using SSH.

## Secrets Configuration

To properly enable the pipeline and deployment, you need to configure the following secrets in GitHub.

More details about these secrets can be found in the [SECRETS.md](docs/SECRETS.md) file.

## Variables Configuration

To properly configure the application, you need to set the following variables in the `.env.example` file.

More details about these variables can be found in the [VARIABLES.md](docs/VARIABLES.md) file.

## Documentation

The `docs` directory contains additional documentation for the project:

**SECRETS.md**: Provides information on the secrets needed for deployment, including the required environment variables and their configuration.

**STYLEGUIDE.md**: Contains guidelines for code style and formatting, including best practices for writing clean, readable code.

**VARIABLES.md**: Describes the variables needed for integration and deployment, including environment variables for the application and Docker service.

## Source Code

The `src` directory contains the project's source code:

**.env.example**: Example environment variables file for Docker. This file should be renamed to `.env` and adjusted with the necessary variables for the project.

**main.py**: The main script that runs the application. This is where the project's entry point is located.

**requirements.txt**: File listing the Python dependencies needed for the project. This file is used to install the required libraries via pip.

## Tests

The `tests` directory contains the project's test scripts. These tests can be run using the following command:

```bash
pytest src/tests/
```

> [!NOTE]
> Actually there are no tests but they will be added in the future.

The tests are automatically run as part of the CI/CD pipeline to ensure the project's functionality is maintained.
