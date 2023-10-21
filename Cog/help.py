from discord.ext import commands
import discord

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def helps(self, ctx):
        """これとは別のHelpを送信します"""
        embed = discord.Embed(title="ヘルプ", description="使用可能なコマンドのリストです", color=0x00ff00)
        embed.add_field(name="!set_channels [メッセージを送るチャンネル] [そのメッセージを転送するチャンネル]", value="チャンネルを設定します", inline=False)
        embed.add_field(name="remove_channels [source_channel]", value="設定したチャンネルを無効化させます", inline=False)
        embed.add_field(name="!helps", value="このヘルプを送信します", inline=False)
        await ctx.send(embed=embed)
