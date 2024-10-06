def generate_memory_prompt(post_action_stm, current_short_term_memory):
    return [{
        "role": "user", 
        "content": f"""
I am a human memory simulator. I will be given my current short-term memory and new information.
I have to update my short-term memory using the new information without losing the old. I can forget unnecessary information.
I need to make the summary as compact as possible and pack in as much information as possible.
If any information or experience is important, or if I learn a new fact or knowledge, I can extract that as long-term memory to store.
Long-term memory can be episodic (the moments) or semantic (knowledge or facts).
If I want to recall something that I might need according to the current observation, I should find queries to recall.
Now Begin \n\n

Input:
Previous Short-Term Memory: {current_short_term_memory} \n
New Information: {post_action_stm} \n

Provide the output in the following tags: \n

<short_term_memory></short_term_memory> \n
<long_term_memory></long_term_memory> \n
<recall_queries></recall_queries> \n

Ensure my response is only the well-formatted output, with no additional text.

Here is my output:
"""
    }]

def generate_response_prompt(identity, long_term_memory, short_term_memory, sensory_memory, action_list):
    return [{
        "role": "user", 
        "content": f"""
{identity} \n\n

I am thinking: {short_term_memory} \n\n
I recalled: {long_term_memory} \n\n
What I see right now: {sensory_memory} \n\n

The actions I can take: {", ".join(action_list)} \n\n

Based on my memory, thoughts, plan, and intent, I will choose an appropriate action.
I will output my action in the following format: \n
<action>
{{
    "action": "chosen_action_name",
    "params": {{
        "param1": "value1",
        "param2": "value2"
    }}
}}
</action> \n\n

I will also summarize "what I observed, what I did, and why I did that. What will I do next?" in the tag below.
<post_action_stm>
</post_action_stm>

Ensure my response is properly formatted.

Here is my output:
"""
    }]
