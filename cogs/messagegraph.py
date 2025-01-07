import discord
from discord.ext import commands
from datetime import datetime, timedelta
import io

import matplotlib.pyplot as plt

class MessageGraph(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="messagegraph", description="指定されたチャンネルの過去24時間の1時間ごとのメッセージ数をグラフにします")
    async def messagegraph_command(self, interaction: discord.Interaction, channel: discord.TextChannel):
        await interaction.response.defer()

        try:
            now = datetime.utcnow()
            one_day_ago = now - timedelta(days=1)
            message_counts = [0] * 24

            async for message in channel.history(after=one_day_ago, limit=None):
                hour = (message.created_at - one_day_ago).seconds // 3600
                message_counts[hour] += 1

            hours = [f"{i}:00" for i in range(24)]
            plt.figure(figsize=(10, 5))
            plt.bar(hours, message_counts, color='blue')
            plt.xlabel('Hour of the Day (UTC)')
            plt.ylabel('Message Count')
            plt.title(f'Message Count per Hour in #{channel.name}')
            plt.xticks(rotation=45)
            plt.tight_layout()

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            file = discord.File(buffer, filename='messagegraph.png')

            await interaction.followup.send(file=file)
        except Exception as e:
            await interaction.followup.send(f"エラーが発生しました: {e}")

async def setup(bot):
    await bot.add_cog(MessageGraph(bot))