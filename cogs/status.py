import asyncio
import time

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands


class Status(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="status", description="ボットのステータスを確認します")
    async def status(self, interaction: discord.Interaction):
        # Discord APIレイテンシを取得
        discord_latency = round(self.bot.latency * 1000, 2)  # 秒 → ミリ秒

        # ネットワークルーターレイテンシを計測
        router_latency = await self.ping_router("192.168.1.1")

        # レスポンスを埋め込みで作成
        embed = discord.Embed(
            title="Swiftly ステータス",
            color=discord.Color.blue()
        )
        embed.add_field(name="Discord APIレイテンシ", value=f"{discord_latency}ms", inline=False)
        embed.add_field(name="ネットワークルーターレイテンシ", value=f"{router_latency}ms", inline=False)
        embed.add_field( name="ステータス詳細", value="[こちらをご覧ください](https://status.sakana11.org)", inline=False)

        await interaction.response.send_message(embed=embed)

    async def ping_router(self, router_ip):
        """ルーターレイテンシを計測"""
        try:
            start_time = time.time()
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://{router_ip}", timeout=3):
                    pass  # レスポンスデータは不要
            latency = round((time.time() - start_time) * 1000, 2)  # 秒 → ミリ秒
            return latency
        except aiohttp.ClientError:
            return "接続エラー"
        except asyncio.TimeoutError:
            return "タイムアウト"


async def setup(bot: commands.Bot):
    """Cogを非同期で追加"""
    await bot.add_cog(Status(bot))
