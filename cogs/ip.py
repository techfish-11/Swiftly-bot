import discord
from discord.ext import commands
import aiohttp
import asyncio

class IP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ip", description="IP情報を取得します")
    async def ip(self, interaction: discord.Interaction, ip_addr: str) -> None:
        await interaction.response.defer()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://ip.evex.land/{ip_addr}") as response:
                    if response.status == 200:
                        data = await response.json()
                        embed = discord.Embed(
                            title="IP Information",
                            description=f"IP: {ip_addr}",
                            color=discord.Color.blue()
                        )
                        fields = [
                            ("Continent", f"{data.get('continent')} ({data.get('continentCode')})"),
                            ("Country", f"{data.get('country')} ({data.get('countryCode')})"),
                            ("Region", f"{data.get('regionName')} ({data.get('region')})"),
                            ("City", data.get("city")),
                            ("ZIP Code", data.get("zip")),
                            ("Coordinates", f"Lat: {data.get('lat')}, Lon: {data.get('lon')}"),
                            ("Timezone", f"{data.get('timezone')} (Offset: {data.get('offset')})"),
                            ("Currency", data.get("currency")),
                            ("ISP", data.get("isp")),
                            ("Organization", data.get("org")),
                            ("AS", f"{data.get('as')} ({data.get('asname')})"),
                            ("Network Type", f"Mobile: {data.get('mobile')}\nProxy: {data.get('proxy')}\nHosting: {data.get('hosting')}")
                        ]
                        for name, value in fields:
                            if value:
                                embed.add_field(name=name, value=value, inline=True)
                        embed.set_footer(text="API Powered by Evex")
                        await interaction.followup.send(embed=embed)
                    else:
                        await interaction.followup.send(f"APIエラー: ステータスコード {response.status}", ephemeral=True)
        except aiohttp.ClientError as e:
            await interaction.followup.send(f"ネットワークエラーが発生しました: {str(e)}", ephemeral=True)
        except asyncio.TimeoutError:
            await interaction.followup.send("リクエストがタイムアウトしました。", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"予期せぬエラーが発生しました: {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(IP(bot))