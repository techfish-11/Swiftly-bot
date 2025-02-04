import discord
from discord.ext import commands
from discord import app_commands
import wikipedia
import re
import asyncio
from functools import lru_cache
from typing import Optional, Tuple, List


class WikipediaCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        wikipedia.set_lang("ja")
        self._cache = {}

    def sanitize_input(self, content: str) -> str:
        """メンションなどの無効化"""
        # メンションの無効化: @ → 全角＠に変換、@everyone, @hereを無効化
        sanitized = re.sub(r'@', '＠', content)
        sanitized = re.sub(r'@(everyone|here)', '＠\\1',
                           sanitized)  # @everyone, @hereを無効化
        return sanitized

    @lru_cache(maxsize=100)
    def _get_cached_search(self, query: str) -> List[str]:
        """検索結果をキャッシュする"""
        return wikipedia.search(query, results=3)

    async def _get_page_info(self, title: str) -> Tuple[str, str, str]:
        """ページ情報を非同期で取得"""
        loop = asyncio.get_event_loop()
        try:
            page = await loop.run_in_executor(None, wikipedia.page, title)
            summary = await loop.run_in_executor(None, wikipedia.summary, title, 3)
            return page.title, summary, page.url
        except Exception as e:
            raise e

    @app_commands.command(name="wikipedia", description="Wikipediaで検索します")
    async def wikipedia_search(self, interaction: discord.Interaction, query: str):
        """Wikipediaで検索し、結果をDiscordに送信します。"""
        await interaction.response.defer()
        query = self.sanitize_input(query)

        try:
            # キャッシュされた検索を使用
            search_results = self._get_cached_search(query)
            if not search_results:
                await interaction.followup.send(f"**'{query}'** に該当する結果はありませんでした。")
                return

            # 非同期でページ情報を取得
            title, summary, url = await self._get_page_info(search_results[0])

            embed = discord.Embed(
                title=title,
                description=summary,
                url=url,
                color=discord.Color.blue()
            )
            embed.set_footer(text="情報はWikipediaより取得されました。")
            await interaction.followup.send(embed=embed)

        except wikipedia.exceptions.DisambiguationError as e:
            options = e.options[:5]
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
            await interaction.followup.send("エラーが発生しました")


async def setup(bot: commands.Bot):
    """Cogを非同期で追加するためのセットアップ関数"""
    await bot.add_cog(WikipediaCog(bot))
