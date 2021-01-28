import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = commands.Bot(command_prefix = '$')

@client.event
async def on_ready():
    print("{} has connected to Discord!".format(client.user.name))


@client.command(name = 'play')
async def play(ctx, url: str):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name = 'General')
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    await voiceChannel.connect()


client.run(TOKEN)
