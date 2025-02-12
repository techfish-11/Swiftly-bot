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
            user = await self.bot.fetch_user(message.author.id)
            if (user.avatar is None or user.created_at.replace(tzinfo=timezone.utc).astimezone(JST).date() == datetime.now(JST).date()) and not message.author.bot:
                await message.delete()
                await message.channel.send(f"{message.author.mention}、デフォルトのアバターおよび今日作成されたアカウントではメッセージを送信できません。")

async def setup(bot):
    await bot.add_cog(iconcheck(bot))
