import discord
import datetime
import youtube_dl
import spotipy
import os
import re
import spotipy.oauth2 as oauth2
import time

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from discord.ext import commands
from os import system
from utils.shuffle import shuffle
from utils.ytUrls import createUrl
from utils.nameSong import createName

load_dotenv()


class music(commands.Cog):
    def __init__(self, bot):

        self.bot = bot
        self.auth_manager = SpotifyClientCredentials(
            os.getenv('CLIENT_ID'), os.getenv('CLIENT_SECRET'))
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)
        self.music_quote = []

        self.ffmpef_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        self.ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': 'True'
        }

    def play_next(self):
        self.music_quote.pop(0)
        if len(self.music_quote) > 0:

            video_url = createUrl(createName(self.music_quote))
                
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                url2 = info['formats'][0]['url']

            voice = discord.utils.get(self.bot.voice_clients)

            voice.play(discord.FFmpegPCMAudio(
                url2, **self.ffmpef_options), after=lambda e: self.play_next())

    def play_nextYT(self):
        self.music_quote.pop(0)
        
        if len(self.music_quote) > 0:
            url2 = self.music_quote[0]
            voice = discord.utils.get(self.bot.voice_clients)
            voice.play(discord.FFmpegPCMAudio(
                url2, **self.ffmpef_options), after=lambda e: self.play_nextYT())

    @commands.command()
    async def play(self, ctx, *, search):
        

        if ctx.message.author.voice == None:
            await ctx.send("Necesitas estar en un canal de voz para poder poner musica!")
            return

        voice_channel = ctx.message.author.voice.channel

        if re.search("https:", search):
            video_url = search
        else:
            video_url = createUrl(search)
            await ctx.send(video_url)

        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            url2 = info['formats'][0]['url']

        if len(self.music_quote) > 0:
            self.music_quote.append(url2)
            return await ctx.send(f"{search}" + " " + "agregado a la cola")

        if ctx.voice_client is None:
            vc = await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
            vc = ctx.voice_client

        self.music_quote.append(url2)
        voice = discord.utils.get(self.bot.voice_clients)

        if not voice.is_playing():
            voice.play(discord.FFmpegPCMAudio("songs/siu.mp3"))
            time.sleep(1.2)
            voice.pause()

        voice.play(discord.FFmpegPCMAudio(url2, **self.ffmpef_options),
                   after=lambda e: self.play_nextYT())

    @commands.command()
    async def pause(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("No hay un audio sonando.")

    @commands.command()
    async def playlist(self, ctx, *, search):

        if ctx.message.author.voice == None:
            await ctx.send("Necesitas estar en un canal de voz para poder poner musica!")
            return

        result = self.sp.playlist(
            search, fields=None, market=None, additional_types=('track', ))
        self.music_quote = result['tracks']['items']
        self.music_quote = shuffle(self.music_quote)

        voice_channel = ctx.message.author.voice.channel

        video_url = createUrl(createName(self.music_quote))

        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            url2 = info['formats'][0]['url']

        if ctx.voice_client is None:
            vc = await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
            vc = ctx.voice_client

        voice = discord.utils.get(self.bot.voice_clients)

        if not voice.is_playing():
            voice.play(discord.FFmpegPCMAudio("songs/siu.mp3"))
            time.sleep(1.2)
            voice.pause()

        voice.play(discord.FFmpegPCMAudio(url2, **self.ffmpef_options),
                   after=lambda e: self.play_next())

    @commands.command()
    async def next(self, ctx):
        if len(self.music_quote) > 0:
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

            if voice.is_playing():
                voice.pause()
                voice.play(discord.FFmpegPCMAudio("songs/siu.mp3"))
                time.sleep(1.2)
                voice.pause()
                self.play_next()

    @commands.command()
    async def song(self, ctx):
        try:
            embed = discord.Embed(
                title=f"{ctx.guild.name}", 
                description="Estas escuchando" + " " +  f"{createName(self.music_quote)}", 
                timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=f"{self.music_quote[0]['track']['album']['images'][0]['url']}")
            await ctx.send(embed=embed)
        except:
            await ctx.send("No hay nada sonando o a ucurrido un error :s")

    @commands.command()
    async def resume(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("El audio no esta en pausa.")

    @commands.command()
    async def disconnect(self, ctx):
        try:
            self.music_quote.clear()
            await ctx.send("Hasta la proxima perros")

            await ctx.voice_client.disconnect()
        except:
            await ctx.send("El bot no se encuentra en un canal")
