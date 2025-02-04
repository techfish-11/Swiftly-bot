import discord
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ping", description="pingを返します")
    async def ping(self, interaction: discord.Interaction) -> None:
        latency = self.bot.latency * 1000  # Convert to milliseconds

        embed = discord.Embed(
            title="Pong!",
            description=f"Bot Latency: {latency:.2f}ms",
            color=discord.Color.green()
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Ping(bot))
