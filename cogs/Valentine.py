import discord
from discord.ext import commands
import random

class Valentine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="choco", description="チョコレートを受け取ります")
    async def give_choco(self, interaction: discord.Interaction) -> None:
        chocolates = [
            "🍫 ミルクチョコレート",
            "🍫 ダークチョコレート",
            "🍫 ホワイトチョコレート",
            "🍫 ストロベリーチョコレート",
            "🍫 ミントチョコレート"
        ]
        choco = random.choice(chocolates)
        await interaction.response.send_message(f"{interaction.user.mention}さん、バレンタインデーに{choco}を受け取りました！")

async def setup(bot):
    await bot.add_cog(Valentine(bot))