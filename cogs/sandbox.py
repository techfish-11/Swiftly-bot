import discord
import aiohttp
from discord.ext import commands

class Sandbox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='sandbox', description='Executes JavaScript or TypeScript code and returns the result.')
    async def sandbox(self, ctx: discord.Interaction, code: str, language: str = 'javascript') -> None:
        await ctx.response.defer(thinking=True)
        url = 'https://js-sandbox.evex.land/'
        headers = {'Content-Type': 'application/json'}
        payload = {'code': code, 'language': language}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        result = await response.text()
                        embed = discord.Embed(title="Sandbox Execution Result", description=f'```{result}```', color=discord.Color.green())
                        embed.set_footer(text="API Powered by EvexDevelopers | Support Server: https://discord.gg/evex")
                        await ctx.followup.send(embed=embed)
                    else:
                        embed = discord.Embed(title="Error", description="Failed to execute code.", color=discord.Color.red())
                        embed.set_footer(text="API Powered by EvexDevelopers | Support Server: https://discord.gg/evex")
                        await ctx.followup.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="Exception", description=str(e), color=discord.Color.red())
            embed.set_footer(text="API Powered by EvexDevelopers | Support Server: https://discord.gg/evex")
            await ctx.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Sandbox(bot))