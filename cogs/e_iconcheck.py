import discord
from discord.ext import commands
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))

class IconCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:  # BOTはスキップ
            return

        if message.guild and message.guild.id == 1255359848644608035:
            user = message.author

            # デフォルトアバターのチェック
            is_default_avatar = user.avatar is None

            # アカウント作成日が今日かどうかのチェック
            created_at_utc = user.created_at.replace(tzinfo=timezone.utc)
            is_new_account = created_at_utc.date() == datetime.now(timezone.utc).date()

            if is_default_avatar or is_new_account:
                await message.delete()
                await message.channel.send(
                    f"{user.mention}、デフォルトのアバターまたは本日作成されたアカウントではメッセージを送信できません。"
                )

async def setup(bot):
    await bot.add_cog(IconCheck(bot))
