import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from Cog.transfer import TransferCog  
from Cog.ping import PingCog  
from Cog.help import HelpCog

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

class JapaneseHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()
        self.commands_heading = "コマンド:"
        self.no_category = "その他"
        self.command_attrs["help"] = "コマンド一覧と簡単な説明を表示"

    def get_ending_note(self):
        return (f"各コマンドの説明: !help <コマンド名>\n"
                f"各カテゴリの説明: !help <カテゴリ名>\n")
    
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", help_command=JapaneseHelpCommand(), intents=intents)

@bot.command(name='reload')
@commands.is_owner()
async def _reload(ctx, extension_name: str):
    """Bot管理者専用コマンド"""
    try:
        bot.reload_extension(extension_name)
        await ctx.send(f'{extension_name} をリロードしました。')
    except Exception as e:
        await ctx.send(f'{extension_name} のリロード中にエラーが発生しました：{e}')

@bot.event
async def on_ready():
    await bot.add_cog(TransferCog(bot))
    await bot.add_cog(PingCog(bot))
    await bot.add_cog(HelpCog(bot))
    print(f'Logged in as {bot.user.name}')
    
if __name__ == '__main__':
    bot.run(TOKEN)