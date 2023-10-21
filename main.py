import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from Cog.transfer import TransferCog  
from Cog.ping import PingCog  

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.add_cog(TransferCog(bot))
    await bot.add_cog(PingCog(bot))
    print(f'Logged in as {bot.user.name}')

if __name__ == '__main__':
    bot.run(TOKEN)