from typing import List
from .memory import update_and_fetch_memory
from .prompts import generate_response_prompt
from services.llm import generate_completion
import json
import re
import asyncio

# Configuration for memory
SENSORY_MEMORY_SIZE = 20

def load_identity():
    try:
        with open("brain/state/character_config.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

class Brain:
    def __init__(self):
        self.short_term_memory = ""
        self.post_action_stm = None
        self.identity = load_identity()
        self.long_term_memory = []

    async def update_and_fetch_memory(self, current_observation, post_action_stm):
        self.short_term_memory, self.long_term_memory = await update_and_fetch_memory(current_observation, post_action_stm, self.short_term_memory)

    async def perceive_and_act(self, observation: str, actions: dict) -> dict:
        # Update memory and fetch long-term memory
        await self.update_and_fetch_memory(observation, self.post_action_stm)
        
        # Act
        sensory_memory = observation

        action_list = []
        for action, params in actions.items():
            param_list = ", ".join([f"{param}={param_type}" for param, param_type in params.items()])
            action_list.append(f"{action}({param_list})")
        
        response_prompt = generate_response_prompt(self.identity, self.long_term_memory, self.short_term_memory, sensory_memory, action_list)
        
        try:
            response = generate_completion(response_prompt, model_type="deep", max_tokens=2000)
            print("LLM Response:", response)
        except Exception as e:
            print("Error generating completion:", e)
            response = None

        # Ensure response is valid and contains actionable data
        if response is None:
            print("Invalid response received from LLM, retrying...")
            return {"action": None, "params": {}}

        # Extract the content within labeled tags
        action_match = re.search(r'<action>(.*?)</action>', response, re.DOTALL)
        rationale_match = re.search(r'<rationale>(.*?)</rationale>', response, re.DOTALL)
        post_action_stm_match = re.search(r'<post_action_stm>(.*?)</post_action_stm>', response, re.DOTALL)

        chosen_action = json.loads(action_match.group(1).strip()) if action_match else {"action": None, "params": {}}
        rationale = rationale_match.group(1).strip() if rationale_match else ""
        post_action_stm = post_action_stm_match.group(1).strip() if post_action_stm_match else ""

        # Update post_action_stm for next cycle
        self.post_action_stm = post_action_stm
        
        return chosen_action