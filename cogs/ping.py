import discord
from discord.ext import commands
from ping3 import ping

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='ping', description='Replies with pong and latency.')
    async def ping(self, interaction: discord.Interaction) -> None:
        latency = self.bot.latency * 1000  # Convert to milliseconds

        # Function to ping a host
        async def ping_host(host):
            try:
                delay = ping(host, timeout=2)
                if delay is None:
                    return f"Failed to ping {host}: No response"
                return f"Ping to {host}: {delay * 1000:.2f}ms"
            except Exception as e:
                return f"Error pinging {host}: {str(e)}"

        # Ping the router and host server
        router_ping = await ping_host('192.168.1.1')
        server_ping = await ping_host('192.168.1.125')

        embed = discord.Embed(
            title="Pong!",
            description=f"Bot Latency: {latency:.2f}ms\n\nNetwork Router Ping\n{router_ping}\n\nHost Server Ping\n{server_ping}",
            color=discord.Color.green()
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Ping(bot))