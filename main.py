import os
import asyncio
from services.setup import load_env_vars
from environment.environment import Environment, State
from environment.phone import Phone
from services.discord_handler import DiscordHandler
from brain.brain import Brain

# Load environment variables and update API keys
load_env_vars()

async def simulate(env, brain):
    while True:
        sensory_info = await env.get_sensory_information()
        # print("Sensory Information: ", sensory_info)
        available_actions = env.get_available_actions()
        # print("Available Actions: ", available_actions)

        # Use Brain to choose an action
        chosen_action = await brain.perceive_and_act(sensory_info, available_actions)
        action_name = chosen_action.get('action')
        action_params = chosen_action.get('params', {})

        # print(f"Chosen Action: {action_name} with Params: {action_params}")

        if action_name not in available_actions:
            # print("Invalid action chosen by the brain. Trying again.")
            continue

        result = env.perform_action(action_name, action_params)
        if result:
            print(result)
        await asyncio.sleep(7)

async def main():
    env = Environment()

    # Add initial states
    env.add_state(State("root", "You have notifications on your phone.", {"open_phone": {"next_state": "phone", "params": {}}}))
    env.add_state(Phone())

    # Initialize the Discord handler
    token = os.getenv('DISCORD_TOKEN')
    handler = DiscordHandler(token, env)

    # Initialize the Brain
    brain = Brain()

    # Run the simulate function and the Discord handler concurrently
    await asyncio.gather(
        handler.run(),
        simulate(env, brain)
    )

# Run the main coroutine
asyncio.run(main())
