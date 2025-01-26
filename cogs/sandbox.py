import discord
import aiohttp
import time
from discord.ext import commands

class Sandbox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @discord.app_commands.command(name='sandbox', description='Executes JavaScript code and returns the result.')
    async def sandbox(self, ctx: discord.Interaction, code: str) -> None:
        await ctx.response.defer(thinking=True)
        url = 'https://js-sandbox.evex.land/'
        headers = {'Content-Type': 'application/json'}
        payload = {'code': code}

        try:
            start_time = time.monotonic()
            async with self.session.post(url, json=payload, headers=headers) as response:
                end_time = time.monotonic()
                elapsed_time = end_time - start_time

                if response.status == 200:
                    result = await response.text()
                    embed = discord.Embed(title="Sandbox Execution Result", description=f'```{result}```', color=discord.Color.green())
                    embed.add_field(name="Execution Time", value=f'{elapsed_time:.2f} seconds', inline=False)
                    embed.set_footer(text="API Powered by EvexDevelopers | Support Server: https://discord.gg/evex")
                    await ctx.followup.send(embed=embed)
                else:
                    embed = discord.Embed(title="Error", description="Failed to execute code.", color=discord.Color.red())
                    embed.add_field(name="Execution Time", value=f'{elapsed_time:.2f} seconds', inline=False)
                    embed.set_footer(text="API Powered by EvexDevelopers | Support Server: https://discord.gg/evex")
                    await ctx.followup.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="Exception", description=str(e), color=discord.Color.red())
            embed.set_footer(text="API Powered by EvexDevelopers | Support Server: https://discord.gg/evex")
            await ctx.followup.send(embed=embed)

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

async def setup(bot):
    await bot.add_cog(Sandbox(bot))