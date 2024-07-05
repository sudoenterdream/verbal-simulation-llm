class State:
    def __init__(self, name, sensory_information, actions):
        self.name = name
        self.sensory_information = sensory_information
        self.actions = actions

    async def get_sensory_information(self):
        return self.sensory_information

    def get_available_actions(self):
        return {action: details['params'] for action, details in self.actions.items()}

    def perform_action(self, action, params=None):
        if action in self.actions:
            return self.actions[action]['next_state']
        return None


class Environment:
    def __init__(self):
        self.states = {}
        self.current_state = None

    def add_state(self, state):
        self.states[state.name] = state
        if not self.current_state:
            self.current_state = state

    async def get_sensory_information(self):
        return await self.current_state.get_sensory_information()

    def get_available_actions(self):
        return self.current_state.get_available_actions()

    def perform_action(self, action, params=None):
        next_state_name = self.current_state.perform_action(action, params)
        if next_state_name and next_state_name in self.states:
            self.current_state = self.states[next_state_name]
            return f"Performed action: {action}"
        return "Invalid action."
