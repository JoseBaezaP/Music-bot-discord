import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from commands.music import music
from commands.info import info

load_dotenv()

bot = commands.Bot(command_prefix = '?', description = "Este es mi primer bot")

bot.add_cog(music(bot))
bot.add_cog(info(bot))


@bot.event
async def on_ready():
  print("The bot is ready")

bot.run(os.getenv('DISCORD_TOKEN'))