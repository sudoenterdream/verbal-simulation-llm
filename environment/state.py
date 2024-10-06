class State:
    def __init__(self, name, sensory_information, actions):
        self.name = name
        self.sensory_information = sensory_information
        self.actions = actions

    async def get_sensory_information(self):
        return self.sensory_information

    def get_available_actions(self):
        return self.actions

    async def perform_action(self, action, params=None):
        if action in self.actions:
            return self.actions[action]["next_state"]
        else:
            raise ValueError(f"Action {action} is not available in state {self.name}")