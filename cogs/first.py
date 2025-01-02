import discord
from discord.ext import commands

class FirstComment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='first-comment', description='このチャンネルの最初のメッセージへのリンクを取得します。')
    async def first_comment(self, interaction: discord.Interaction):
        channel = interaction.channel
        try:
            first_message = None
            async for message in channel.history(limit=1, oldest_first=True):
                first_message = message
                break
            if first_message:
                await interaction.response.send_message(f"このチャンネルの最初のメッセージ: {first_message.jump_url}")
            else:
                await interaction.response.send_message("このチャンネルにはメッセージが見つかりませんでした。")
        except Exception as e:
            await interaction.response.send_message(f"エラーが発生しました: {e}")

async def setup(bot):
    await bot.add_cog(FirstComment(bot))