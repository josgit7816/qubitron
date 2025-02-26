import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import requests

load_dotenv()

TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
VOICE_CHANNEL_ID = int(os.getenv("VOICE_CHANNEL_ID"))

# https://api.mistral.ai/v1/chat/completions

# Replace 'MISTRAL_API_URL' with the actual API endpoint of Mistral AI
# MISTRAL_API_URL = 'https://api.mistral.ai/v1/chat'
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# Replace 'YOUR_MISTRAL_API_KEY' with your actual Mistral API key
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Replace 'YOUR_BOT_TOKEN' with your bot's token
# TOKEN = 'YOUR_BOT_TOKEN'

# Set up intents
intents = discord.Intents.default()  # Enable default intents
intents.message_content = True  # Enable access to message content (if needed)

# Set up the bot with a command prefix
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: When the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print("------")

    # El bot se une automáticamente al canal de voz
    guild = bot.get_guild(GUILD_ID)
    if guild:
        channel = guild.get_channel(VOICE_CHANNEL_ID)
        if channel:
            await channel.connect()
            print(f"Bot conectado al canal de voz: {channel.name}")


# Command: Respond to !hello
@bot.command(name="hello")
async def hello(ctx):
    await ctx.send(f"Hello, {ctx.author.name}!")


@bot.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == bot.user:
        return

    # Check if the message starts with a specific prefix, e.g., '!mistral'
    if message.content.startswith("!mistral"):
        user_input = message.content[len("!mistral") :].strip()
        print("user inpun:", user_input)

        # Send the user input to Mistral AI
        response = requests.post(
            MISTRAL_API_URL,
            headers={"Authorization": f"Bearer {MISTRAL_API_KEY}"},
            json={
                "model": "mistral-large-latest",
                "messages": [{"role": "user", "content": user_input}]},
        )

        print(response.json())

        if response.status_code == 200:
            #ai_response = response.json().get("output", "No response from Mistral AI")
            ai_response = response.json()["choices"][0]["message"]["content"]
            await message.channel.send(ai_response)
        else:
            # Print the response content for debugging
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            await message.channel.send("Error communicating with Mistral AI")


# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)
