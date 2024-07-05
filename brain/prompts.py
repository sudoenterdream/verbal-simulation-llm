def generate_memory_prompt(current_observation, post_action_stm, current_short_term_memory):
    return [{
        "role": "user", 
        "content": f"""You are an advanced cognitive architecture simulating human-like memory processes. Your task is to dynamically update and manage a complex memory system based on new inputs and existing information. Process the given data carefully and output a structured memory state.

Input:
Current Observation: {current_observation}
Previous Short-Term Memory: {current_short_term_memory}
Post-Action Short-Term Memory: {post_action_stm}

Instructions:
1. Analyze the input thoroughly, identifying key information, patterns, and relationships.
2. Update the short-term memory by integrating new observations with existing thoughts. Prioritize recent and salient information while maintaining overall coherence.
3. Extract significant events, insights, or learnings for long-term memory storage. Consider both episodic (event-based) and semantic (factual) information.
4. Generate relevant queries to prompt recall of associated long-term memories that may be pertinent to the current situation.

Provide your output in the following format:
<short_term_memory>
Concise yet comprehensive summary of current active thoughts, incorporating new observations and relevant previous information
</short_term_memory>
<long_term_memory>
Significant episodic memory entry
Important semantic knowledge gained
Any other notable long-term memory formation
</long_term_memory>
<recall_queries>
Specific query to retrieve relevant long-term memory 1
Specific query to retrieve relevant long-term memory 2
</recall_queries>

Ensure your response is only the well-formatted output, with no additional text."""
    }]

def generate_response_prompt(identity, long_term_memory, short_term_memory, sensory_memory, action_list):
    return [{
        "role": "user", 
        "content": f"""You are an advanced AI agent with the following identity:
{identity}

Current Cognitive State:
1. Long-Term Memory Recall: {long_term_memory}
2. Short-Term Memory (Active Thoughts): {short_term_memory}
3. Current Sensory Input: {sensory_memory}

Available Actions: {", ".join(action_list)}

Instructions:
1. Carefully analyze your current cognitive state, considering all aspects of your memory and sensory input.
2. Based on this analysis, determine the most appropriate action to take.
3. Provide a detailed rationale for your chosen action, explaining how it aligns with your identity and current state.
4. Format your chosen action and its parameters in JSON.
5. Summarize key information to retain for the next cognitive cycle, including observations, actions, intentions, and thoughts.

Output your response in the following format:

<action>
{{
    "action": "chosen_action_name",
    "params": {{
        "param1": "value1",
        "param2": "value2"
    }}
}}
</action>
<rationale>
Provide a concise explanation for your chosen action here.
</rationale>
<post_action_stm>
- Observation: [Key observation from current state]
- Action Taken: [Summary of chosen action]
- Intention: [Future intention or goal]
- Thought: [Relevant thought or reflection]
</post_action_stm>

Ensure your response contains only these three elements, properly formatted."""
    }]
