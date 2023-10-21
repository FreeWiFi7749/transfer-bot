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

        @bot.command()
        async def set_channels_slash(ctx: commands.Context, source_channel: discord.TextChannel, dest_channel: discord.TextChannel):
            self.channel_mapping[str(source_channel.id)] = dest_channel.id
            self.save_mapping()
            await ctx.respond(f"Set source channel to {source_channel.name} and destination channel to {dest_channel.name}")

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
        self.channel_mapping[str(source_channel.id)] = dest_channel.id
        self.save_mapping()
        await ctx.send(f"Set source channel to {source_channel.name} and destination channel to {dest_channel.name}")

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
                    await webhook.send(
                        content=msg.content, 
                        username=msg.author.display_name, 
                        avatar_url=msg.author.avatar,
                        wait=True
                    )