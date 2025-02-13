import discord
from discord.ext import commands
import aiohttp
import asyncio

class IP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ip", description="IP情報を取得します")
    async def ip(self, interaction: discord.Interaction, ip_addr: str) -> None:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://ip.evex.land/{ip_addr}") as response:
                    if response.status == 200:
                        try:
                            data = await response.json()
                        except aiohttp.ContentTypeError:
                            await interaction.response.send_message("無効な応答形式です。", ephemeral=True)
                            return
                        embed = discord.Embed(
                            title="IP Information",
                            description=f"IP: {ip_addr}",
                            color=discord.Color.blue()
                        )
                        for key, value in data.items():
                            embed.add_field(name=key, value=value, inline=False)
                        embed.set_footer(text="API Powered by Evex")
                        await interaction.response.send_message(embed=embed)
                    else:
                        await interaction.response.send_message("IP情報を取得できませんでした。", ephemeral=True)
        except aiohttp.ClientError:
            await interaction.response.send_message("ネットワークエラーが発生しました。", ephemeral=True)
        except asyncio.TimeoutError:
            await interaction.response.send_message("リクエストがタイムアウトしました。", ephemeral=True)

async def setup(bot):
    await bot.add_cog(IP(bot))