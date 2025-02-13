import discord
from discord.ext import commands
import aiohttp

class IP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ip", description="IP情報を取得します")
    async def ip(self, interaction: discord.Interaction, ip_addr: str) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://ip.evex.land/{ip_addr}") as response:
                if response.status == 200:
                    data = await response.json()
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


async def setup(bot):
    await bot.add_cog(IP(bot))