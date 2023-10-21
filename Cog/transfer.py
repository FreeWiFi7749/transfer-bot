import json
import discord
from discord.ext import commands
from discord import webhook
import aiohttp

class TransferCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_mapping = {}
        self.load_mapping()

    def save_mapping(self):
        with open("channels.json", "w") as f:
            json.dump(self.channel_mapping, f)

    def load_mapping(self):
        try:
            with open("channels.json", "r") as f:
                self.channel_mapping = json.load(f)
        except FileNotFoundError:
            pass  

    @commands.command()
    async def set_channels(self, ctx, source_channel: discord.TextChannel, dest_channel: discord.TextChannel):
        """チャンネルを設定します"""
        self.channel_mapping[str(source_channel.id)] = dest_channel.id
        self.save_mapping()
        await ctx.send(f"{source_channel.mention}のメッセージを{dest_channel.mention}に送信します")

    @commands.command()
    async def remove_channels(self, ctx, source_channel: discord.TextChannel):
        """設定したチャンネル設定を消去します"""
        if str(source_channel.id) in self.channel_mapping:
            del self.channel_mapping[str(source_channel.id)]
            self.save_mapping()
            await ctx.send(f"{source_channel.mention}のメッセージの転送を停止しました")
        else:
            await ctx.send(f"{source_channel.mention}は設定されていません")

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author == self.bot.user:
            return

        dest_channel_id = self.channel_mapping.get(str(msg.channel.id))
        if dest_channel_id:
            dest_channel = self.bot.get_channel(dest_channel_id)
            if dest_channel:
                webhooks = await dest_channel.webhooks()
                webhook = webhooks[0] if webhooks else await dest_channel.create_webhook(name='Transfer Webhook')

                async with aiohttp.ClientSession() as session:
                    if msg.content:  # メッセージが空でない場合のみ送信
                        await webhook.send(
                            content=msg.content, 
                            username=msg.author.display_name, 
                            avatar_url=msg.author.avatar,
                            wait=True
                        )
                    elif msg.attachments:  # 添付ファイルがある場合、それを送信
                        for attachment in msg.attachments:
                            await webhook.send(
                                content=f"{msg.author.display_name} が添付ファイルを送信しました",
                                avatar_url=msg.author.avatar,
                                wait=True,
                                file=await attachment.to_file()
                            )