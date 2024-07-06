def generate_memory_prompt(post_action_stm, current_short_term_memory):
    return [{
        "role": "user", 
        "content": f"""
You are human memory simulator. You will be given current short term memory and new information.
You have to update the short term memory using new information without losing old. You can forget unecessary information.
Make the summary as compact as possible, and pack in as much information as possible.
Also If any information/Experience is important, or you learn new fact / knowledge, you can extract that as long term memory to store.
Long term memory can be episodic (the moments) or semantic (knowledge / facts).
If you want to recall something that you might need according to current observation, find queries to recall.
Now Begin \n\n

Input:
Previous Short-Term Memory: {current_short_term_memory} \n
New Information: {post_action_stm} \n

Provide the output in the following tags: \n

<short_term_memory></short_term_memory> \n
<long_term_memory></long_term_memory> \n
<recall_queries></recall_queries> \n

Ensure your response is only the well-formatted output, with no additional text."""
    }]

def generate_response_prompt(identity, long_term_memory, short_term_memory, sensory_memory, action_list):
    return [{
        "role": "user", 
        "content": f"""
{identity} \n\n

You are thinking: {short_term_memory} \n\n
You recalled: {long_term_memory} \n\n
What you see right now: {sensory_memory} \n\n

The actions you can take: {", ".join(action_list)} \n\n

Based on your memory, thoughts, plan, intent choose appropriate action.
Output your action in the following format: \n
<action>
{{
    "action": "chosen_action_name",
    "params": {{
        "param1": "value1",
        "param2": "value2"
    }}
}}
</action> \n\n

Also summarize "what you observed, what you did and why you did that. what will you do next?" in the tag below.
<post_action_stm>
</post_action_stm>

Ensure your response properly formatted."""
    }]