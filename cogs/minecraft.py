import discord
from discord import app_commands
import aiohttp
from discord.ext import commands

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='minecraft', description='Get the status of a Minecraft server')
    async def minecraft(self, interaction: discord.Interaction, address: str):
        url = f'https://api.mcsrvstat.us/3/{address}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

                if data['online']:
                    embed = discord.Embed(title=f"Server Status for {address}", color=discord.Color.green())
                    embed.add_field(name="IP", value=data.get('ip', 'N/A'))
                    embed.add_field(name="Port", value=data.get('port', 'N/A'))
                    embed.add_field(name="Version", value=data.get('version', 'N/A'))
                    embed.add_field(name="Players Online", value=f"{data['players']['online']}/{data['players']['max']}")
                    if 'hostname' in data:
                        embed.add_field(name="Hostname", value=data['hostname'])
                    if 'motd' in data:
                        embed.add_field(name="MOTD", value="\n".join(data['motd']['clean']))
                    if 'plugins' in data:
                        plugins = ", ".join([plugin['name'] for plugin in data['plugins']])
                        embed.add_field(name="Plugins", value=plugins)
                    if 'mods' in data:
                        mods = ", ".join([mod['name'] for mod in data['mods']])
                        embed.add_field(name="Mods", value=mods)
                else:
                    embed = discord.Embed(title=f"Server Status for {address}", color=discord.Color.red())
                    embed.add_field(name="Status", value="Offline")

                await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Minecraft(bot))