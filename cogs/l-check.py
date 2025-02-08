import discord
from discord.ext import commands
import random

class LoveChecker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='love-checker')
    async def love_checker(self, ctx, user: discord.User):
        # Simple algorithm to calculate love percentage
        random.seed(user.id + ctx.author.id)
        love_percentage = random.randint(0, 100)

        embed = discord.Embed(
            title="Love Checker",
            description=f"{user.mention}さんからの恋愛感情は{love_percentage}%です！",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(LoveChecker(bot))