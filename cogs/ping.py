import discord
from discord.ext import commands
import asyncio
import subprocess

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='ping', description='Replies with pong and latency.')
    async def ping(self, interaction: discord.Interaction) -> None:
        latency = self.bot.latency * 1000  # Convert to milliseconds

        # Function to ping a host
        async def ping_host(host):
            proc = await asyncio.create_subprocess_shell(
                f'ping -n 1 {host}',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, _ = await proc.communicate()
            return stdout.decode()

        # Ping the router and host server
        router_ping = await ping_host('192.168.1.1')
        server_ping = await ping_host('192.168.1.125')

        embed = discord.Embed(
            title="Pong!",
            description=f"Bot Latency: {latency:.2f}ms",
            color=discord.Color.green()
        )
        embed.add_field(name="Network Router Ping", value=router_ping, inline=False)
        embed.add_field(name="Host Server Ping", value=server_ping, inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Ping(bot))