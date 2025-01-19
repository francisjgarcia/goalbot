# Variables Configuration

This file contains the necessary configurations for the integration and deployment of the application. Make sure to keep this information secure and do not share it publicly.

## Environment Variables

### Application Configuration Variables

- **`DEBUG`**:
  - **Description**: A boolean value that determines whether the application is running in debug mode.
  - **Example**: `True`

- **`OPENAI_MODEL_ID`**:
  - **Description**: The ID of the OpenAI model to use for generating responses.
  - **Example**: `gpt-3.5-turbo`

- **`OPENAI_RANDOM_PROMPT`**:
  - **Description**: The prompt to use for generating random responses.
  - **Example**: `Generate a random response.`

- **`OPENAI_GOALS_MOTIVATION_PROMPT`**:
  - **Description**: The prompt to use for generating responses related to goals and motivation.
  - **Example**: `Generate a response about goals and motivation.`

- **`OPENAI_NON_PARTICIPANT_USER_PROMPT`**:
  - **Description**: The prompt to use for generating responses related to non-participant users.
  - **Example**: `Generate a response about non-participant users.`

- **`OPENAI_GENERAL_SUMMARY_PROMPT`**:
  - **Description**: The prompt to use for generating general summaries.
  - **Example**: `Generate a general summary.`

- **`OPENAI_INDIVIDUAL_SUMMARY_PROMPT`**:
  - **Description**: The prompt to use for generating individual summaries.
  - **Example**: `Generate an individual summary.`

- **`TWITCH_STREAMER_NAME`**:
  - **Description**: The name of the Twitch streamer to monitor.
  - **Example**: `mytwitchstreamer`

### Docker Configuration Variables

- **`DOCKER_MEMORY_LIMIT`**:
  - **Description**: The memory limit for the Docker container.
  - **Example**: `50M`

- **`DOCKER_MEMORY_RESERVATION`**:
  - **Description**: The memory reservation for the Docker container.
  - **Example**: `10M`
