import discord
from discord.ext import commands

class FirstComment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.first_message_cache = {}  # チャンネルごとのキャッシュ

    @discord.app_commands.command(name='first-comment', description='このチャンネルの最初のメッセージへのリンクを取得します。')
    async def first_comment(self, interaction: discord.Interaction):
        channel = interaction.channel
        try:
            # キャッシュが存在する場合はそれを利用する
            if channel.id in self.first_message_cache:
                first_message = self.first_message_cache[channel.id]
            else:
                first_message = None
                async for message in channel.history(limit=1, oldest_first=True):
                    first_message = message
                    break
                # キャッシュへ保存（存在する場合のみ）
                if first_message:
                    self.first_message_cache[channel.id] = first_message
                    
            if first_message:
                embed = discord.Embed(
                    title="最初のメッセージ",
                    description=f"[こちら]({first_message.jump_url}) をクリックして最初のメッセージに移動します。",
                    color=discord.Color.blue()
                )
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message("このチャンネルにはメッセージが見つかりませんでした。")
        except Exception as e:
            await interaction.response.send_message(f"エラーが発生しました: {e}")

async def setup(bot):
    await bot.add_cog(FirstComment(bot))