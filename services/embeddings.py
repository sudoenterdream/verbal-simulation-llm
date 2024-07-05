import requests

JINA_API_KEY = None

def update_jina_key(api_key):
    global JINA_API_KEY
    JINA_API_KEY = api_key

def get_embeddings(text):
    url = 'https://api.jina.ai/v1/embeddings'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {JINA_API_KEY}'
    }
    data = {
        'input': [
            {"text": text}
        ],
        'model': 'jina-clip-v1',
        'encoding_type': 'float'
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()['data'][0]['embedding']
