import discord
from discord.ext import commands

class FirstComment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='first-comment', description='Get the link to the first message in the channel.')
    async def first_comment(self, interaction: discord.Interaction):
        channel = interaction.channel
        try:
            first_message = None
            async for message in channel.history(limit=1, oldest_first=True):
                first_message = message
                break
            if first_message:
                await interaction.response.send_message(f"The first message in this channel: {first_message.jump_url}")
            else:
                await interaction.response.send_message("No messages found in this channel.")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(FirstComment(bot))