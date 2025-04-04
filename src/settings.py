import os

# General settings
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Discord settings
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')

# OpenAI settings
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL_ID = os.getenv('OPENAI_MODEL_ID')
OPENAI_RANDOM_PROMPT = os.getenv('OPENAI_RANDOM_PROMPT')
OPENAI_GOALS_MOTIVATION_PROMPT = os.getenv(
    'OPENAI_GOALS_MOTIVATION_PROMPT'
)
OPENAI_NON_PARTICIPANT_USER_PROMPT = os.getenv(
    'OPENAI_NON_PARTICIPANT_USER_PROMPT'
)
OPENAI_GENERAL_SUMMARY_PROMPT = os.getenv(
    'OPENAI_GENERAL_SUMMARY_PROMPT'
)
OPENAI_INDIVIDUAL_SUMMARY_PROMPT = os.getenv(
    'OPENAI_INDIVIDUAL_SUMMARY_PROMPT'
)

# Twitch settings
TWITCH_ACCESS_TOKEN = os.getenv('TWITCH_ACCESS_TOKEN')
TWITCH_STREAMER_NAME = os.getenv('TWITCH_STREAMER_NAME')
