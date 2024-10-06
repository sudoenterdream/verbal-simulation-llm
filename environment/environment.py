from datetime import datetime
from .phone import Phone
from .virtual_space import VirtualSpace
from .apps.arxiv_app import ArxivApp

class Environment:
    def __init__(self):
        self.states = {}
        self.current_state = None
        self.add_state(VirtualSpace())
        self.add_state(Phone())
        self.add_state(ArxivApp("arxiv_app", self)) # fix the env passing later


    def add_state(self, state):
        self.states[state.name] = state
        if not self.current_state:
            self.current_state = state

    async def get_sensory_information(self):
        temporal_info = datetime.now().strftime("%d %B %Y (%I:%M %p)")
        return temporal_info + "\n" + await self.current_state.get_sensory_information()

    def get_available_actions(self):
        return self.current_state.get_available_actions()

    async def perform_action(self, action, params=None):
        next_state_name = await self.current_state.perform_action(action, params)
        if next_state_name and next_state_name in self.states:
            self.current_state = self.states[next_state_name]
            return f"Performed action: {action}"
        return "Invalid action."
