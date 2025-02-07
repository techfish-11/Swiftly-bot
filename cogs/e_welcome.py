import yaml

import discord
from discord.ext import commands


class MemberWelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self._read_yml()

        self.GUILD_ID = self.config["GUILD_ID"]
        self.CHANNEL_ID = self.config["CHANNEL_ID"]
        self.TARGET_MEMBER_INCREMENT = self.config["TARGET_MEMBER_INCREMENT"]

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild.id != self.GUILD_ID:
            return
        print("member join")

        guild = self.bot.get_guild(self.GUILD_ID)
        channel = guild.get_channel(self.CHANNEL_ID)

        if guild is not None and channel is not None:
            remainder = len(guild.members) % self.TARGET_MEMBER_INCREMENT
            if remainder == 0:
                message = (
                    f"🎉🎉🎉 お祝い 🎉🎉🎉\n"
                    f"{member.mention} さん、ようこそ！\n"
                    f"{len(guild.members)}人達成！\n"
                    f"{guild.name}のメンバーが{len(guild.members)}人になりました！皆さんありがとうございます！"
                )
                await channel.send(message)
            else:
                remaining_members = self.TARGET_MEMBER_INCREMENT - remainder
                message = (
                    f"ようこそ！\n"
                    f"{member.mention} さん、ようこそ！\n"
                    f"現在のメンバー数: {len(guild.members)}人。\n"
                    f"あと {remaining_members} 人で {len(guild.members) + remaining_members}人達成です！"
                )
                await channel.send(message)

    def _read_yml(self):
        """ Load configuration from evex.yml """
        with open("evex.yml", "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        return config


async def setup(bot: commands.Bot):
    await bot.add_cog(MemberWelcomeCog(bot))
