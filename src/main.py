import json
import time
import logging
import random
import asyncio
import discord
import signal
import sys
from openai import OpenAI
from twitchio.ext import commands
import settings


# Logger setup to differentiate between bots
def setup_logger(name):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        f'%(asctime)s - {name} - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


# Logger for the Discord bot
discord_logger = setup_logger('DiscordBot')
# Logger for the Twitch bot
twitch_logger = setup_logger('TwitchBot')


# Reusable function to interact with OpenAI
async def openai_get_response(prompt, message="",
                              model=settings.OPENAI_MODEL_ID,
                              max_tokens=300, temperature=1.2):
    """
    This function interacts with the OpenAI API
    and returns a generated response.

    :param prompt: The prompt passed to OpenAI.
    :param message: The message passed to OpenAI.
    :param model: The model used in the API.
    :param max_tokens: The maximum number of tokens to generate.
    :param temperature: The level of creativity in the response (0 is
                         deterministic, 2 is more random).
    :return: The message generated by OpenAI.
    """
    # Create an instance of the OpenAI client
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    # Call the OpenAI API
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt},
                  {"role": "system", "content": message}],
        max_tokens=max_tokens,
        temperature=temperature
    )

    # Return the generated response
    return response.choices[0].message.content


# Class for the Discord bot
class DiscordBot:
    def __init__(self):
        self.intents = discord.Intents.default()
        self.intents.guilds = True
        self.intents.messages = True
        self.intents.message_content = True
        self.intents.guild_messages = True

        self.bot = discord.Client(intents=self.intents)
        self.channel_id = int(settings.DISCORD_CHANNEL_ID)

        self.bot_started_check = asyncio.Event()

        # Associate the on_ready event with the bot instance
        self.bot.event(self.on_ready)

    async def on_ready(self):
        discord_logger.info(
            f'Bot connected as {self.bot.user} with ID {self.bot.user.id}'
        )
        self.bot_started_check.set()

    async def get_forum_posts(self):
        await self.bot_started_check.wait()
        # Get the forum channel by its ID
        forum_channel = self.bot.get_channel(self.channel_id)

        if isinstance(forum_channel, discord.ForumChannel):
            discord_logger.info(
                f"Searching posts from the forum: {forum_channel.name}"
            )

            # Create the final JSON structure
            result = {
                "forum_name": forum_channel.name,
                "posts": []
            }

            # Iterate through the threads in the forum
            for thread in forum_channel.threads:
                # Exclude the thread with the title "Propósitos 2025"
                if thread.name == "Propósitos 2025":
                    continue

                # Get the author of the first message
                creator = None
                async for message in thread.history(limit=1):
                    creator = message.author  # First message is from creator

                # Initialize the entry for this thread
                thread_data = {
                    "twitch_user": thread.name,  # Thread name as 'twitch_user'
                    "discord_user": creator.name if creator else "Unknown",
                    # Creator of the post
                    "messages": []  # List for the messages within the thread
                }

                # Iterate through the messages in the thread
                async for message in thread.history(limit=None):
                    thread_data["messages"].append({
                        "author": message.author.name,
                        "content": message.content
                    })

                # Add the complete thread to the posts list
                result["posts"].append(thread_data)

            # Convert the dictionary to JSON
            posts_json = json.dumps(result, indent=4, ensure_ascii=False)

            # Print the result
            discord_logger.info(
                f"A total of {len(result['posts'])} posts were retrieved."
            )
            return posts_json
        else:
            discord_logger.error("This channel is not a forum")
            return None

    async def start(self):
        # Start the Discord bot using await instead of run
        await self.bot.start(settings.DISCORD_BOT_TOKEN)


# Class for the Twitch bot
class TwitchBot(commands.Bot):
    def __init__(self, discord_bot):
        super().__init__(
            token=settings.TWITCH_ACCESS_TOKEN, prefix='!',
            initial_channels=[settings.TWITCH_STREAMER_NAME]
        )
        self.streamer_id = None
        self.streamer_online = False
        self.user_message_count = {}
        self.user_trigger_count = {}
        self.last_propositos_use = {}
        self.warning_sent = {}
        self.blocked_users = {}
        self.user_locks = {}
        self.discord_bot = discord_bot
        self.discord_forum_users = []
        self.bot_started_check = asyncio.Event()
        self.streamer_status_checked = asyncio.Event()

    async def event_ready(self):
        twitch_logger.info(
            f'Bot connected as {self.nick} with ID {self.user_id}')
        self.bot_started_check.set()

    async def get_streamer_id(self):
        user = await self.fetch_users(names=[settings.TWITCH_STREAMER_NAME])
        if not self.streamer_id:
            try:
                if user:
                    self.streamer_id = user[0].id
                    twitch_logger.info(
                        "Connected to streamer "
                        f"{settings.TWITCH_STREAMER_NAME} "
                        f"with ID {self.streamer_id}.")
                else:
                    twitch_logger.error(
                        "Not able to find streamer user "
                        f"{settings.TWITCH_STREAMER_NAME}.")
            except Exception as e:
                twitch_logger.error(f"Error getting streamer ID: {e}")
        return self.streamer_id

    async def check_streamer_status(self):
        await self.bot_started_check.wait()
        while True:
            if settings.DEBUG:
                if not self.streamer_online:
                    twitch_logger.debug(
                        "Simulating that streamer "
                        f"{settings.TWITCH_STREAMER_NAME} is online.")
                self.streamer_online = True
            else:
                streamer_id = await self.get_streamer_id()
                streams = await self.fetch_streams(user_ids=[streamer_id])
                if streams:
                    if not self.streamer_online:
                        twitch_logger.info(
                            f"The streamer {settings.TWITCH_STREAMER_NAME} "
                            "is now online.")
                    self.streamer_online = True
                else:
                    if self.streamer_online:
                        twitch_logger.info(
                            f"The streamer {settings.TWITCH_STREAMER_NAME} "
                            "is now offline.")
                    self.streamer_online = False
            self.streamer_status_checked.set()
            if settings.DEBUG:
                await asyncio.sleep(5)
            else:
                await asyncio.sleep(60)

    async def send_random_messages(self):
        await self.streamer_status_checked.wait()
        while True:
            if self.streamer_online:
                if settings.DEBUG:
                    wait_time = random.randint(60, 300)
                else:
                    wait_time = random.randint(1800, 3000)
                await asyncio.sleep(wait_time)

                if self.streamer_online:
                    # Call OpenAI to get a generated message
                    random_message = await openai_get_response(
                        settings.OPENAI_RANDOM_PROMPT)

                    # Send the generated message to the chat
                    for channel in self.connected_channels:
                        await channel.send(random_message)
                    twitch_logger.info(
                        "Auto-generated message sent to "
                        f"{settings.TWITCH_STREAMER_NAME} chat:"
                        f"\n{random_message}"
                    )
                else:
                    await asyncio.sleep(60)
            else:
                if settings.DEBUG:
                    await asyncio.sleep(5)
                else:
                    await asyncio.sleep(60)

    async def update_discord_forum_users(self):
        forum_posts_json = await self.discord_bot.get_forum_posts()
        if forum_posts_json:
            forum_posts = json.loads(forum_posts_json)
            self.discord_forum_users = [
                post['twitch_user'] for post in forum_posts['posts']
            ]
            twitch_logger.info(
                f"Users with goals on Discord: {self.discord_forum_users}")
        else:
            twitch_logger.error("Could not fetch posts from Discord.")

    async def event_message(self, message):
        if message.author is None:
            return

        if message.author.name.lower() == self.nick.lower():
            return

        user = message.author.name

        # Create a Lock for the user if it doesn't exist
        if user not in self.user_locks:
            self.user_locks[user] = asyncio.Lock()

        # Create a message count for the user if it doesn't exist
        async with self.user_locks[user]:
            if user not in self.user_message_count:
                self.user_message_count[user] = 0
                if settings.DEBUG:
                    self.user_trigger_count[user] = 1
                else:
                    self.user_trigger_count[user] = random.randint(10, 20)

            self.user_message_count[user] += 1

            if self.user_message_count[user] >= self.user_trigger_count[user]:
                await self.update_discord_forum_users()

                if user in self.discord_forum_users:
                    discord_json = await self.discord_bot.get_forum_posts()
                    discord_json_load = json.loads(discord_json)
                    filtered_posts = [
                        post for post in discord_json_load['posts']
                        if post['twitch_user'] == f'{user}'
                    ]
                    resume_user_message = await openai_get_response(
                        settings.OPENAI_GOALS_MOTIVATION_PROMPT,
                        str(filtered_posts)
                    )
                    await message.channel.send(f"{resume_user_message}")
                    twitch_logger.info(
                        f"Send user {user} a message with their goals:"
                        f"\n{resume_user_message}"
                    )
                else:
                    non_participant_user_message = await openai_get_response(
                        settings.OPENAI_NON_PARTICIPANT_USER_PROMPT, user)
                    await message.channel.send(
                        f"{non_participant_user_message}")
                    twitch_logger.info(
                        f"Asking user {user} to participate in proposals "
                        f"through Discord:\n{non_participant_user_message}"
                    )

                self.user_trigger_count[user] = float('inf')

        await self.handle_commands(message)

    async def block_user(self, ctx):
        current_time = time.time()
        user_name = ctx.author.name

        # Create a Lock for the user if it doesn't exist
        if user_name not in self.user_locks:
            self.user_locks[user_name] = asyncio.Lock()

        # Acquire the Lock for the user
        async with self.user_locks[user_name]:
            if (user_name in self.warning_sent or
                    user_name in self.blocked_users):
                return

            if user_name in self.last_propositos_use:
                last_used = self.last_propositos_use[user_name]
                if current_time - last_used < 5:
                    if user_name not in self.warning_sent:
                        message_list = [
                            f"¡Espérate un momento, {user_name}! "
                            "Ya usaste el comando hace poquito. 🚫",
                            f"¡Tranquilo, {user_name}! No puedes usar "
                            "el comando tan rápido, ¡sé paciente! ⏳",
                            f"¡Ay, ay, ay, {user_name}! ¿Ya otra vez? "
                            "Tienes que esperar un ratito. 🐢",
                            f"¡Relájate, {user_name}! El comando no se "
                            "va a ir a ningún lado, calma. 😅",
                            f"¡No te aceleres, {user_name}! Tienes que "
                            "hacer una pausa antes de repetir el "
                            "comando. 🕐",
                            f"¡Párale, {user_name}! Tu dedo necesita "
                            "descansar de tanto apretar el comando. ✋",
                            f"¡Un poco de paciencia, {user_name}! ¡No se "
                            "vale hacer trampa y usarlo tan rápido! 🤫",
                            f"¡Vas muy rápido, {user_name}! El comando no "
                            "es un sprint, ¡relájate! 🏃‍♂️",
                            f"Echa el freno madaleno, {user_name}! No "
                            "puedes usar el comando tan seguido. 🛑"
                        ]
                        random_message = random.choice(message_list)
                        await ctx.send(random_message)
                        twitch_logger.info(
                            f"User {user_name} was warned about using the "
                            f"command too quickly:\n{random_message}")
                        self.warning_sent[user_name] = True
                        return
                    else:
                        self.blocked_users[user_name] = current_time
                        twitch_logger.info(
                            f"User {user_name} was blocked for using "
                            "the command too quickly.")
                        return

            self.last_propositos_use[user_name] = current_time

    # Method to block users for a certain amount of time
    async def unlock_blocked_users(self):
        await self.streamer_status_checked.wait()
        while True:
            if self.streamer_online:
                if settings.DEBUG:
                    wait_time = 5
                else:
                    wait_time = 300
                await asyncio.sleep(wait_time)
                self.blocked_users.clear()
                twitch_logger.info("Blocked users list cleared.")
            else:
                if settings.DEBUG:
                    await asyncio.sleep(5)
                else:
                    await asyncio.sleep(60)

    @commands.command(name='propositos')
    async def propositos(self, ctx, user: str = None):
        if self.streamer_online:
            if user is None:
                # Block the user if they are using the command too quickly
                await self.block_user(ctx)
                if (ctx.author.name in self.warning_sent or
                        ctx.author.name in self.blocked_users):
                    return
                # Call Discord bot function to get the JSON
                discord_json = await self.discord_bot.get_forum_posts()
                if discord_json:
                    # Now pass the JSON to OpenAI to get the summary
                    summary = await openai_get_response(
                        settings.OPENAI_GENERAL_SUMMARY_PROMPT,
                        str(discord_json)
                    )
                    # Send the summary in parts if it's too long
                    await self.send_large_message(ctx, f"{summary}")
                    twitch_logger.info(
                        "Summary generated by OpenAI sent to Twitch chat:"
                        f"\n{summary}"
                    )
                else:
                    twitch_logger.error("Could not fetch posts from Discord.")
            else:
                # Block the user if they are using the command too quickly
                await self.block_user(ctx)
                if (ctx.author.name in self.warning_sent or
                        ctx.author.name in self.blocked_users):
                    return
                await self.update_discord_forum_users()
                if user not in self.discord_forum_users:
                    await ctx.send(
                        f"El usuario {user} no ha publicado sus propósitos "
                        "en Discord.")
                    twitch_logger.info(
                        f"User {user} has not posted their goals on Discord.")
                else:
                    discord_json = await self.discord_bot.get_forum_posts()
                    discord_json_load = json.loads(discord_json)
                    filtered_posts = [
                        post for post in discord_json_load['posts']
                        if post['twitch_user'] == f'{user}'
                    ]
                    resume_user_message = await openai_get_response(
                        settings.OPENAI_INDIVIDUAL_SUMMARY_PROMPT,
                        str(filtered_posts)
                    )
                    await self.send_large_message(
                        ctx, f"{resume_user_message}")
                    twitch_logger.info(
                        "Summary generated by OpenAI sent to Twitch chat:"
                        f"\n{resume_user_message}")
        else:
            twitch_logger.info(
                f"Ignored !propositos command because "
                f"{settings.TWITCH_STREAMER_NAME} is offline."
            )

    # Method to send a large message in parts
    async def send_large_message(self, ctx, message):
        # Split the message into parts of 500 characters
        max_message_length = 500
        for i in range(0, len(message), max_message_length):
            # Send a fragment of the message
            await ctx.send(message[i:i + max_message_length])


# Main function to start both bots
async def main():
    discord_bot = DiscordBot()
    twitch_bot = TwitchBot(discord_bot)

    # Keep the bots running
    await asyncio.gather(
        twitch_bot.start(),  # This task handles the Twitch bot
        discord_bot.start(),  # This task handles the Discord bot
        twitch_bot.check_streamer_status(),  # Run streamer status check
        twitch_bot.send_random_messages(),  # Run random message sending
        twitch_bot.unlock_blocked_users()  # Run user unlock task
    )

    # Other Twitch bot methods...
    async def close(self):
        # Perform cleanup tasks if necessary
        await self._ws.close()


# Function to handle controlled shutdown when Ctrl+C is pressed
def signal_handler(signal, frame):
    print("Interrupt received, closing the script...")
    try:
        asyncio.get_event_loop().stop()
    except Exception as e:
        print(f"Error closing async tasks: {e}")
    sys.exit(0)


# Bind the signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)


# Start the asyncio event loop
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Script interrupted by user (Ctrl+C). Closing...")
