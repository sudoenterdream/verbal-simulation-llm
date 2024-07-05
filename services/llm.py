from groq import Groq

client = None

def update_groq_key(api_key):
    global client
    client = Groq(api_key=api_key)

def select_model(model_type):
    if model_type == 'deep':
        return "llama3-70b-8192"
    elif model_type == 'fast':
        return "llama3-8b-8192"
    else:
        raise ValueError(f"Unknown model type: {model_type}")

def generate_completion(messages, model_type="fast", temperature=1, max_tokens=10000, stop="[end]"):
    if client is None:
        raise ValueError("Groq client is not initialized. Please set the API key using update_groq_key().")

    model = select_model(model_type)

    response = client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content

# import ollama

# def generate_completion(messages, model_type="fast", temperature=1, max_tokens=10000, stop="[end]"):
#     # if client is None:
#     #     raise ValueError("Groq client is not initialized. Please set the API key using update_groq_key().")

#     # model = select_model(model_type)

#     # response = client.chat.completions.create(
#     #     messages=messages,
#     #     model=model,
#     #     temperature=temperature,
#     #     max_tokens=max_tokens,
#     # )
#     response = ollama.chat(model='phi3:mini', messages=messages)
#     # return response.choices[0].message.content
#     return response['message']['content']



