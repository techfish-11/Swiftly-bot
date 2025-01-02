import discord
from discord.ext import commands
import aiohttp

class Time(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='time', description='現在の時間を取得します。')
    async def fetch_time(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api1.sakana11.org/api/ntp') as response:
                if response.status == 200:
                    data = await response.json()
                    time = data.get('time')
                    embed = discord.Embed(title="現在の時間", description=f"現在の時間は: {time}", color=discord.Color.blue())
                    embed.add_field(name="APIエンドポイント", value='https://api1.sakana11.org/api/ntp', inline=False)
                    await interaction.response.send_message(embed=embed)
                else:
                    await interaction.response.send_message('APIから時間を取得できませんでした。')

async def setup(bot):
    await bot.add_cog(Time(bot))