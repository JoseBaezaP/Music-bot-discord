import discord
import datetime
import os

from dotenv import load_dotenv
from discord.ext import commands
from os import system

load_dotenv()


class info(commands.Cog):
    def __init__(self, bot):

        self.bot = bot
     
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(
            title=f"{ctx.guild.name}", description="Cree este bot por todo ya que no sirven otros bots :c", timestamp=datetime.datetime.utcnow())
        await ctx.send(embed=embed)