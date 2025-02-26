import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN =  os.getenv('TOKEN')
GUILD_ID = int(os.getenv("GUILD_ID"))
VOICE_CHANNEL_ID = int(os.getenv("VOICE_CHANNEL_ID"))

# Replace 'YOUR_BOT_TOKEN' with your bot's token
#TOKEN = 'YOUR_BOT_TOKEN'

# Set up intents
intents = discord.Intents.default()  # Enable default intents
intents.message_content = True  # Enable access to message content (if needed)

# Set up the bot with a command prefix
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: When the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')

        # El bot se une automáticamente al canal de voz
    guild = bot.get_guild(GUILD_ID)
    if guild:
        channel = guild.get_channel(VOICE_CHANNEL_ID)
        if channel:
            await channel.connect()
            print(f"Bot conectado al canal de voz: {channel.name}")

# Command: Respond to !hello
@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.name}!')

# Run the bot
if __name__ == '__main__':
    bot.run(TOKEN)