import discord
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='ping', description='Replies with pong and latency.')
    async def ping(self, ctx: discord.Interaction) -> None:
        latency = self.bot.latency * 1000  # Convert to milliseconds
        await ctx.response.send_message(f'Pong! Latency: {latency:.2f}ms')

async def setup(bot):
    await bot.add_cog(Ping(bot))