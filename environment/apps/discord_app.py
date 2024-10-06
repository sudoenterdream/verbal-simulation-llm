import asyncio
from datetime import datetime
from ..state import State

class DiscordChat(State):
    def __init__(self, name, bot_name, channel, handler):
        self.bot_name = bot_name
        self.channel = channel
        self.handler = handler
        actions = {
            "send_message": {
                "next_state": name,
                "params": {
                    "message": "string"
                }
            },
            "exit_chat": {
                "next_state": "discord_home",
                "params": {}
            },
            "wait_for_response": {
                "next_state": name,
                "params": {
                    "seconds": "int"
                }
            }
        }
        super().__init__(name, "", actions)

    async def fetch_latest_messages(self):
        messages = await self.handler.get_latest_messages(self.channel)
        formatted_history = []
        current_time = datetime.utcnow()
        for timestamp, author, content in messages:
            message_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            if (current_time - message_time).days >= 1:
                formatted_time = message_time.strftime("%d %B")
            else:
                formatted_time = message_time.strftime("%H:%M")
            formatted_entry = f"{formatted_time} - {author}: {content}"
            if author == self.bot_name:
                formatted_entry = f"{formatted_time} - you: {content}"
            formatted_history.append(formatted_entry)
        return "\n".join(formatted_history)

    async def get_sensory_information(self):
        self.sensory_information = f"""
        I am in {self.channel} chat. \n
        I shouldn't send too many messages in a row, but if new messages are below my last message, I'll start talking.
        If no message arrives from others in the last 5 minutes, they must be offline. \n
        I see these messages \n\n

        {await self.fetch_latest_messages()}"""
        return self.sensory_information

    def send_message(self, message):
        asyncio.create_task(self.channel.send(message))  # Send the message to the Discord channel

    async def wait_for_response(self, seconds):
        await asyncio.sleep(min(seconds, 5))  # Wait for specified seconds or 10 seconds maximum

    async def perform_action(self, action, params=None):
        if action == "send_message" and params:
            message = params.get('message')
            if message:
                self.send_message(message)
                return self.name  # Stay in the same state after sending a message
        elif action == "wait_for_response" and params:
            seconds = int(params.get('seconds', 10))  # Default to 10 seconds if not specified, convert to int
            await self.wait_for_response(seconds)
            return self.name  # Stay in the same state after waiting for a response
        return await super().perform_action(action)

class DiscordHome(State):
    def __init__(self, chats, bot_name):
        actions = {f"open_chat_{chat}": {"next_state": f"chat_{chat}", "params": {}} for chat in chats}
        actions["close_discord"] = {"next_state": "phone", "params": {}}
        sensory_information = "No chats available currently." if not chats else f"""
        I am using discord.
        I see these chats: {'\n'.join(chats.keys())}.\n\n

        Some of these are group chats, and some DMs.
        I can open and close chats to switch between chats
        """
        super().__init__("discord_home", sensory_information, actions)
        self.chats = chats
        self.bot_name = bot_name

    def add_chat(self, chat_name, channel, handler):
        chat_state = f"chat_{chat_name}"
        self.chats[chat_state] = DiscordChat(chat_state, self.bot_name, channel, handler)
        self.actions[f"open_chat_{chat_name}"] = {"next_state": chat_state, "params": {}}
        self.update_sensory_information()

    def update_sensory_information(self):
        chats_info = "No chats available." if not self.chats else f"Chats available: {', '.join(self.chats.keys())}."
        self.sensory_information = chats_info
