import discord
from discord.ext import commands
from dotenv import load_dotenv
import openai
import os

# Load environment variables
load_dotenv()

TOKEN = os.getenv('TOKEN')
GUILD_ID = int(os.getenv("GUILD_ID"))
VOICE_CHANNEL_ID = int(os.getenv("VOICE_CHANNEL_ID"))
OPENAI_API_KEY = os.getenv("MISTRAL_API_KEY")

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Initialize bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Configure OpenAI API
openai.api_key = OPENAI_API_KEY

# Function to call OpenAI API (Mistral model)
async def get_ai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="deepseek/deepseek-r1:free",  # Use a Mistral model
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

# Event: Bot Ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    
    # Auto-connect to voice channel
    guild = bot.get_guild(GUILD_ID)
    if guild:
        channel = guild.get_channel(VOICE_CHANNEL_ID)
        if channel:
            try:
                await channel.connect()
                print(f"Bot connected to voice channel: {channel.name}")
            except discord.ClientException:
                print("Bot is already connected.")
            except discord.errors.Forbidden:
                print("No permission to join voice channel.")

# AI-powered command
@bot.command(name='ask')
async def ask(ctx, *, question: str):
    await ctx.send("Thinking... 🤔")
    response = await get_ai_response(question)
    await ctx.send(response)

# Command to disconnect from voice
@bot.command(name='leave')
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from voice channel.")

# Run bot
if __name__ == '__main__':
    bot.run(TOKEN)
