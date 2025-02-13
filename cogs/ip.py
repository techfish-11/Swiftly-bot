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
                        content_type = response.headers.get('Content-Type', '')
                        if 'application/json' not in content_type.lower():
                            await interaction.followup.send(f"予期しない応答形式です: {content_type}", ephemeral=True)
                            return

                        try:
                            data = await response.json()
                        except aiohttp.ContentTypeError:
                            text_response = await response.text()
                            await interaction.followup.send(f"JSONの解析に失敗しました。応答: {text_response[:1000]}", ephemeral=True)
                            return
                            
                        if data.get("status") == "success":
                            embed = discord.Embed(
                                title="IP Information",
                                description=f"IP: {ip_addr}",
                                color=discord.Color.blue()
                            )
                            fields = [
                                ("Continent", data.get("continent")),
                                ("Country", data.get("country")),
                                ("Region", data.get("regionName")),
                                ("City", data.get("city")),
                                ("ZIP Code", data.get("zip")),
                                ("Latitude", data.get("lat")),
                                ("Longitude", data.get("lon")),
                                ("Timezone", data.get("timezone")),
                                ("ISP", data.get("isp")),
                                ("Organization", data.get("org")),
                                ("AS", data.get("as")),
                                ("AS Name", data.get("asname")),
                                ("Mobile", data.get("mobile")),
                                ("Proxy", data.get("proxy")),
                                ("Hosting", data.get("hosting")),
                            ]
                            for name, value in fields:
                                if value is not None:
                                    embed.add_field(name=name, value=value, inline=False)
                            embed.set_footer(text="API Powered by Evex")
                            await interaction.followup.send(embed=embed)
                        else:
                            error_message = data.get("message", "IP情報を取得できませんでした。")
                            await interaction.followup.send(error_message, ephemeral=True)
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