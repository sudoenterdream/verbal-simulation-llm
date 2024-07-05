from services.llm import generate_completion
from .prompts import generate_memory_prompt
import json
import re

async def update_and_fetch_memory(current_observation, post_action_stm, current_short_term_memory):
    memory_prompt = generate_memory_prompt(current_observation, post_action_stm, current_short_term_memory)
    
    try:
        response = generate_completion(memory_prompt, model_type="deep", max_tokens=2000)
        print("Memory LLM Response:", response)
    except Exception as e:
        print("Error generating memory completion:", e)
        response = None

    # Ensure response is valid and contains memory data
    if response is None:
        print("Invalid response received from LLM for memory update, using previous memory...")
        return current_short_term_memory, []

    # Extract the content within labeled tags
    short_term_memory_match = re.search(r'<short_term_memory>(.*?)</short_term_memory>', response, re.DOTALL)
    long_term_memory_match = re.search(r'<long_term_memory>(.*?)</long_term_memory>', response, re.DOTALL)
    recall_queries_match = re.search(r'<recall_queries>(.*?)</recall_queries>', response, re.DOTALL)

    short_term_memory = short_term_memory_match.group(1).strip() if short_term_memory_match else current_short_term_memory
    long_term_memory = [entry.strip() for entry in long_term_memory_match.group(1).strip().split('\n') if long_term_memory_match] if long_term_memory_match else []
    recall_queries = [query.strip() for query in recall_queries_match.group(1).strip().split('\n') if recall_queries_match] if recall_queries_match else []

    # Write the new short-term memory to the file
    with open("brain/state/short_term_memory.txt", "w") as file:
        file.write(short_term_memory)
    
    return short_term_memory, long_term_memory
