import discord
from discord.ext import commands
from environment.apps.discord_app import DiscordHome, DiscordChat

class DiscordHandler:
    def __init__(self, token, environment):
        self.token = token
        self.environment = environment
        intents = discord.Intents.default()
        intents.message_content = True
        intents.dm_messages = True  # Ensure the bot can read DM messages
        intents.members = True  # Ensure the bot can access member data
        self.bot = commands.Bot(command_prefix="!", intents=intents)
        self.discord_home = None
        self.phone = None

    async def on_ready(self):
        print(f'Logged in as {self.bot.user}')
        bot_name = self.bot.user.name
        # Get list of text channels in servers
        chats = {}
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                chat_name = f"{guild.name}/{channel.name}"
                chats[chat_name] = channel

        # Get list of DM channels
        for member in self.bot.get_all_members():
            if member.bot:
                continue  # Skip other bots
            if member.dm_channel is None:
                try:
                    await member.create_dm()
                except Exception as e:
                    print(f"Failed to create DM for {member.name}: {e}")
                    continue
            chat_name = f"DM/{member.name}"
            chats[chat_name] = member.dm_channel

        discord_home = DiscordHome(chats, bot_name, self)
        self.environment.add_state(discord_home)
        self.discord_home = discord_home
        for chat_name, channel in chats.items():
            self.environment.add_state(DiscordChat(f"chat_{chat_name}", bot_name, channel, self))

        self.phone = self.environment.states['phone']

    async def get_latest_messages(self, channel):
        messages = []
        try:
            async for message in channel.history(limit=20):
                messages.append(f"{message.author.name}: {message.content}")
            messages.reverse()  # To keep the latest messages at the end
        except Exception as e:
            print(f"Failed to get messages for {channel}: {e}")
        return messages

    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if isinstance(message.channel, discord.DMChannel):
            chat_name = f"DM/{message.author.name}"
        else:
            chat_name = f"{message.guild.name}/{message.channel.name}"
        
        # Increment notification count
        self.discord_home.increment_notification(chat_name)

        user_message = f'{message.author.name}: {message.content}'
        chat_state = f"chat_{chat_name}"
        print('updated')

    def update_phone_notifications(self, count):
        self.phone.update_notifications('discord', count)

    async def run(self):
        @self.bot.event
        async def on_ready():
            await self.on_ready()

        @self.bot.event
        async def on_message(message):
            await self.on_message(message)

        await self.bot.start(self.token)

def update_discord_key(token):
    DiscordHandler.token = token