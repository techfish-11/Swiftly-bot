import discord
from discord.ext import commands
from discord import app_commands
import re

class MojiBake(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def sanitize_input(self, content: str) -> str:
        """入力された文字列からメンションを無効化する"""
        sanitized = re.sub(r'@', '＠', content)  # すべての@を全角に置き換え
        sanitized = re.sub(r'@(everyone|here)', '＠\\1', sanitized)  # @everyone, @hereも無効化
        return sanitized

    @app_commands.command(name="moji-bake", description="文字をわざと文字化けさせます")
    async def moji_bake(self, interaction: discord.Interaction, content: str):
        """ユーザーから受け取った文字列を文字化けさせる"""
        try:
            # メンションを無効化
            sanitized_content = self.sanitize_input(content)

            # UTF-8にエンコード → ISO-8859-1でデコード（文字化け）
            content_baked = sanitized_content.encode('utf-8').decode('iso-8859-1')

            # さらにShift_JISで文字化けを追加（エラーを無視して処理）
            content_baked = content_baked.encode('utf-8').decode('shift_jis', errors='ignore')

        except UnicodeDecodeError as e:
            content_baked = f"文字化け処理中にエラーが発生しました: {str(e)}"
        except Exception as e:
            content_baked = f"予期しないエラーが発生しました: {str(e)}"

        # メンション無効化設定を追加して返す
        await interaction.response.send_message(content_baked, allowed_mentions=discord.AllowedMentions.none())

async def setup(bot: commands.Bot):
    """Cogを非同期で追加"""
    await bot.add_cog(MojiBake(bot))