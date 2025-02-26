import discord
import requests
from dotenv import load_dotenv
import os   
load_dotenv()   

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = os.getenv('TOKEN')

# Replace 'MISTRAL_API_URL' with the actual API endpoint of Mistral AI
MISTRAL_API_URL = 'https://api.mistral.ai/v1/chat'

# Replace 'YOUR_MISTRAL_API_KEY' with your actual Mistral API key
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return

    # Check if the message starts with a specific prefix, e.g., '!mistral'
    if message.content.startswith('!mistral'):
        user_input = message.content[len('!mistral'):].strip()
        print("user inpun:", user_input)

        # Send the user input to Mistral AI
        response = requests.post(
            MISTRAL_API_URL,
            headers={'Authorization': f'Bearer {MISTRAL_API_KEY}'},
            json={'input': user_input}
        )

        print(response)

        if response.status_code == 200:
            ai_response = response.json().get('output', 'No response from Mistral AI')
            await message.channel.send(ai_response)
        else:
            await message.channel.send('Error communicating with Mistral AI')

client.run(TOKEN)
