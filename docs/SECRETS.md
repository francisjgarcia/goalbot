# Secrets Configuration

This file contains sensitive configurations necessary for the integration and deployment of the application. Make sure to keep this information secure and do not share it publicly.

## Github Actions

### Workflow Secrets

- **`SSH_PRIVATE_HOST`**:
  - **Description**: The hostname or IP address of the private SSH server you need to connect to.
  - **Example**: `ssh.example.com`

- **`SSH_PRIVATE_KEY`**:
  - **Description**: The private SSH key used for authentication when accessing remote servers.
  - **Example**: `-----BEGIN OPENSSH PRIVATE KEY----- ... -----END OPENSSH PRIVATE KEY-----`

- **`SSH_PRIVATE_PORT`**:
  - **Description**: The port number on the private SSH server to connect to.
  - **Example**: `22`

- **`SSH_PRIVATE_USER`**:
  - **Description**: The username for authentication on the private SSH server.
  - **Example**: `deploy`

- **`SSH_PROXY_HOST`**:
  - **Description**: The hostname or IP address of the proxy server.
  - **Example**: `proxy.example.com`

- **`SSH_PROXY_PORT`**:
  - **Description**: The port number on the proxy server to connect to.
  - **Example**: `8080`

- **`SSH_PROXY_USER`**:
  - **Description**: The username for authentication on the proxy server.
  - **Example**: `proxyuser`

### Application Configuration Variables

- **`DISCORD_BOT_TOKEN`**:
  - **Description**: The token for the Discord bot.
  - **Example**: `mydiscordbottoken`

- **`DISCORD_CHANNEL_ID`**:
  - **Description**: The ID of the Discord channel where the bot will send messages.
  - **Example**: `12345678987654321`
  - **Note**: You can get the channel ID by right-clicking on the channel name and selecting "Copy ID".

- **`OPENAI_API_KEY`**:
  - **Description**: The API key for the OpenAI GPT-3 service.
  - **Example**: `myopenaiapikey`

- **`TWITCH_ACCESS_TOKEN`**:
  - **Description**: The access token for the Twitch API.
  - **Example**: `mytwitchaccesstoken`
