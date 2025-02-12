import discord
from discord.ext import commands
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))

class iconcheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild.id == 1255359848644608035:
            if (message.author.avatar == message.author.default_avatar and
                message.author.created_at.date() == datetime.now(JST).date()):
                await message.delete()
                await message.channel.send(f"{message.author.mention}、デフォルトのアバターおよび今日作成されたアカウントではメッセージを送信できません。")

async def setup(bot):
    await bot.add_cog(iconcheck(bot))