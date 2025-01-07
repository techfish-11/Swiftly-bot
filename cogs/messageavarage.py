import discord
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio

class MessageAverage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="messageaverage", description="過去24時間の1時間ごとの平均メッセージ数を計算します")
    async def message_average_command(self, interaction: discord.Interaction):
        now = datetime.utcnow()
        one_day_ago = now - timedelta(days=1)
        message_counts = [0] * 24

        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                try:
                    async for message in channel.history(after=one_day_ago, oldest_first=True):
                        hour_index = (message.created_at - one_day_ago).seconds // 3600
                        message_counts[hour_index] += 1
                except (discord.Forbidden, discord.HTTPException):
                    continue

        average_messages = sum(message_counts) / 24
        embed = discord.Embed(
            title="過去24時間の1時間ごとの平均メッセージ数",
            description=f"平均メッセージ数: {average_messages:.2f}",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(MessageAverage(bot))