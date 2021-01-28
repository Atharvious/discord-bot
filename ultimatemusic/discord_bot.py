import os
import discord
from discord.ext import commands
import random
import ffmpeg
import youtube_dl

from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


bot = commands.Bot(command_prefix='$')

#This is not important as I shifted to a new method of implementing bot functions.
#But this is useful when we want to display errors on discord itself, instead of the console.
@bot.event
async def on_error(event, *args, **kwargs):
    with open('error.log', 'a') as f:
        if event == 'on_message':
            f.write("Unhandled message: {}\n".format(args[0]))
        else:
            raise


#Events are everything that happen on discord, eg- a new text message, or a new person joining the server.
#This event (on_ready) is the event of the bot connecting to the server first time.
@bot.event
async def on_ready():
    print("{} has connected to Discord!".format(bot.user.name))

#Commands are what follow the 'command prefix' which we mentioned when instantiating the client object (like !play , !pause on rhythmbot)
@bot.command()
async def play(ctx, url: str):
    #For now I've just put together a method of downloading the video from the entered link and playing it after converting to mp3. Also, no adding multiple tracks as of now
    song_loc = os.path.isfile("song.mp3")
    try:
        if song_loc:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the end or use the stop command.")
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name = 'General')
    await voiceChannel.connect()
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    #download settingd for yt downloader
    ydl_opts = {
            'format' : 'bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality':'192'}]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file,"song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

#rest is pretty straight-forward
@bot.command(name = 'leave')
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("Nowhere to leave from!")

@bot.command(name = 'resume')
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("Audio is not paused.")




@bot.command(name = 'pause')
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("No audio is playing")

@bot.command(name = 'stop')
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    voice.stop()

#abhi nahi kiya hai ye implement
@bot.command(name = 'next')
async def next(ctx):
    pass


@bot.command(name = 'rtd')
async def rtd(ctx, num_dice: int, num_sides: int):
    dice = [str(random.choice(range(1,num_sides+1))) for _ in range(num_dice)]
    await ctx.send(', '.join(dice))



bot.run(TOKEN)
