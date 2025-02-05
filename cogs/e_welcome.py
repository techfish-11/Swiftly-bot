import discord
from discord.ext import commands
import yaml


class MemberWelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self._read_yml()

        self.GUILD_ID = self.config["GUILD_ID"]
        self.CHANNEL_ID = self.config["CHANNEL_ID"]
        self.TARGET_MEMBER_COUNT = self.config["TARGET_MEMBER_COUNT"]

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild.id != self.GUILD_ID:
            return

        guild = self.bot.get_guild(self.GUILD_ID)
        channel = guild.get_channel(self.CHANNEL_ID)

        if guild is not None and channel is not None:
            remaining_members = self.TARGET_MEMBER_COUNT - len(guild.members)
            if remaining_members > 0:
                embed = discord.Embed(
                    title="ようこそ！",
                    description=(
                        f"{member.mention} さん、ようこそ！\n"
                        f"現在のメンバー数: {len(guild.members)}人。\n"
                        f"あと {remaining_members} 人で {self.TARGET_MEMBER_COUNT}人達成です！"
                    ),
                    color=discord.Color.green()
                )
                embed.set_footer(text="Hosted by techfish")
                await channel.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="ようこそ！",
                    description=f"{member.mention} さん、ようこそ！",
                    color=discord.Color.green()
                )
                embed.set_footer(text="Hosted by techfish")
                await channel.send(embed=embed)

        # 1000人超えたらお祝い
        if len(guild.members) >= self.TARGET_MEMBER_COUNT:
            await self.celebrate_1000_members(guild, channel)

    async def celebrate_1000_members(self, guild, channel):
        embed = discord.Embed(
            title="🎉🎉🎉 お祝い 🎉🎉🎉",
            description=(
                f"{self.TARGET_MEMBER_COUNT}人達成！\n"
                f"{guild.name}のメンバーが{self.TARGET_MEMBER_COUNT}人になりました！皆さんありがとうございます！"
            ),
            color=discord.Color.gold()
        )
        embed.set_footer(text="Hosted by techfish")
        await channel.send(embed=embed)

    def _read_yml(self):
        """ Load configuration from evex.yml """
        with open("evex.yml", "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        return config

    def _write_yml(self):
        """ Save configuration from evex.yml """
        with open("evex.yml", "w", encoding="utf-8") as file:
            yaml.safe_dump(self.config, file, allow_unicode=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(MemberWelcomeCog(bot))
