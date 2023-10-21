from discord.ext import commands

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx):
        """BotのPINGを送信します"""
        await ctx.send(f'Pong! \n{round(self.bot.latency * 1000)}ms')