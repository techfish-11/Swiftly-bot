import discord
from discord.ext import commands
from datetime import datetime

class iconcheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild.id == 1255359848644608035:
            if (message.author.default_avatar_url == message.author.avatar_url and
                message.author.created_at.date() == datetime.utcnow().date()):
                await message.delete()
                await message.channel.send(f"{message.author.mention}、デフォルトのアバターおよび今日作成されたアカウントではメッセージを送信できません。")

def setup(bot):
    bot.add_cog(iconcheck(bot))