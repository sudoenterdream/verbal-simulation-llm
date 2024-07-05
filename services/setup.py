import os
from dotenv import load_dotenv
from services.llm import update_groq_key
from services.embeddings import update_jina_key
from services.discord_handler import update_discord_key

# Load environment variables from the .env file
def load_env_vars():
    load_dotenv()
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    JINA_API_KEY = os.getenv('JINA_API_KEY')
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    
    # Update API keys
    update_groq_key(GROQ_API_KEY)
    update_jina_key(JINA_API_KEY)
    update_discord_key(DISCORD_TOKEN)
