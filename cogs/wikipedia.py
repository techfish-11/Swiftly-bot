import discord
from discord.ext import commands
from discord import app_commands
import wikipedia
import re

class WikipediaCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        wikipedia.set_lang("ja")  # 日本語のWikipediaを使用

    def sanitize_input(self, content: str) -> str:
        """メンションなどの無効化"""
        # メンションの無効化: @ → 全角＠に変換、@everyone, @hereを無効化
        sanitized = re.sub(r'@', '＠', content)  
        sanitized = re.sub(r'@(everyone|here)', '＠\\1', sanitized)  # @everyone, @hereを無効化
        return sanitized

    @app_commands.command(name="wikipedia", description="Wikipediaで検索します")
    async def wikipedia_search(self, interaction: discord.Interaction, query: str):
        """Wikipediaで検索し、結果をDiscordに送信します。"""
        await interaction.response.defer()  # 応答を遅延（非同期処理用）
        query = self.sanitize_input(query)  # クエリをサニタイズ

        try:
            # Wikipediaで検索
            search_results = wikipedia.search(query, results=3)
            if not search_results:
                await interaction.followup.send(f"**'{query}'** に該当する結果はありませんでした。")
                return

            # 最初の検索結果のページを取得
            page = wikipedia.page(search_results[0])
            title = page.title
            summary = wikipedia.summary(search_results[0], sentences=3)
            url = page.url

            # Embed形式で送信
            embed = discord.Embed(
                title=title,
                description=summary,
                url=url,
                color=discord.Color.blue()
            )
            embed.set_footer(text="情報はWikipediaより取得されました。")
            await interaction.followup.send(embed=embed)

        except wikipedia.exceptions.DisambiguationError as e:
            # 曖昧な結果が見つかった場合
            options = e.options[:5]  # 最初の5件を表示
            embed = discord.Embed(
                title="曖昧な検索結果",
                description="\n".join(options),
                color=discord.Color.orange()
            )
            embed.set_footer(text="もう一度詳しいキーワードで検索してください。")
            await interaction.followup.send(embed=embed)
        except wikipedia.exceptions.PageError:
            await interaction.followup.send(f"**'{query}'** に該当するページが見つかりませんでした。")
        except Exception as e:
            await interaction.followup.send(f"エラーが発生しました")

async def setup(bot: commands.Bot):
    """Cogを非同期で追加するためのセットアップ関数"""
    await bot.add_cog(WikipediaCog(bot))