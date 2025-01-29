import discord
from discord.ext import commands
import base64
import re

class Base64(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # /base64コマンドの定義
    @discord.app_commands.command(name="base64", description="Base64エンコードまたはデコードします。")
    async def base64_command(self, interaction: discord.Interaction, action: str, content: str):
        if action not in ['encode', 'decode']:
            await interaction.response.send_message("アクションは 'encode' または 'decode' のいずれかでなければなりません。")
            return

        try:
            if action == "encode":
                # UTF-8 エンコードをBase64に変換
                encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
                embed = discord.Embed(title="Base64 エンコード結果", description=encoded, color=discord.Color.blue())
                await interaction.response.send_message(embed=embed)
            elif action == "decode":
                # Base64デコード
                decoded = base64.b64decode(content).decode('utf-8')

                # デコード結果に @everyone やメンションが含まれているかをチェック
                # @everyone とユーザーIDメンション (<@1234567890>) の検出
                if '@everyone' in decoded or re.search(r'<@!?(\d+)>', decoded) or re.search(r'<@&(\d+)>', decoded):
                    await interaction.response.send_message("デコード結果に、@ everyone やメンション、役職メンションが含まれているため、デコードを拒否しました。")
                    return

                embed = discord.Embed(title="Base64 デコード結果", description=decoded, color=discord.Color.green())
                await interaction.response.send_message(embed=embed)
        except base64.binascii.Error:
            # 無効なBase64形式のエラーハンドリング
            await interaction.response.send_message("無効なBase64文字列です。正しい形式で入力してください。")
        except Exception as e:
            # その他のエラー処理
            await interaction.response.send_message(f"エラーが発生しました: {str(e)}")

# Cogのセットアップ
async def setup(bot):
    await bot.add_cog(Base64(bot))