import asyncio
from environment.environment import State

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
            }
        }
        super().__init__(name, "", actions)

    async def fetch_latest_messages(self):
        messages = await self.handler.get_latest_messages(self.channel)
        formatted_history = []
        for entry in messages:
            author, content = entry.split(": ", 1)
            if author == self.bot_name:
                formatted_history.append(f"you : {content}")
            else:
                formatted_history.append(entry)
        return "\n".join(formatted_history)

    async def get_sensory_information(self):
        self.sensory_information = await self.fetch_latest_messages()
        return self.sensory_information

    def send_message(self, message):
        asyncio.create_task(self.channel.send(message))  # Send the message to the Discord channel

    def perform_action(self, action, params=None):
        if action == "send_message" and params:
            message = params.get('message')
            if message:
                self.send_message(message)
                return self.name  # Stay in the same state after sending a message
        return super().perform_action(action)

class DiscordHome(State):
    def __init__(self, chats, bot_name):
        actions = {f"open_chat_{chat}": {"next_state": f"chat_{chat}", "params": {}} for chat in chats}
        actions["close_discord"] = {"next_state": "phone", "params": {}}
        sensory_information = "No chats available." if not chats else f"Chats available: {', '.join(chats.keys())}."
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
