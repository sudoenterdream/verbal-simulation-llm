import os
import asyncio
from services.setup import load_env_vars
from environment.environment import Environment
from environment.state import State
from environment.phone import Phone
from services.discord_handler import DiscordHandler
from brain.brain import Brain

# Load environment variables and update API keys
load_env_vars()

async def simulate(env, brain):
    while True:
        sensory_info = await env.get_sensory_information()
        available_actions = env.get_available_actions()

        # Use Brain to choose an action
        chosen_action = await brain.perceive_and_act(sensory_info, available_actions)
        action_name = chosen_action.get('action')
        action_params = chosen_action.get('params', {})

        if action_name not in available_actions:
            print("Invalid action chosen by the brain. Trying again.")
            continue

        result = await env.perform_action(action_name, action_params)  # Await the perform_action call
        if result:
            print(result)
        await asyncio.sleep(10)

async def main():
    env = Environment()

    # Initialize the Discord handler
    handler = DiscordHandler(env)

    # Initialize the Brain
    brain = Brain()

    # Run the simulate function and the Discord handler concurrently
    await asyncio.gather(
        handler.run(),
        simulate(env, brain)
    )

# Run the main coroutine
asyncio.run(main())
