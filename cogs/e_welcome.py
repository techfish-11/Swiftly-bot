import os
import sqlite3
from datetime import datetime, timedelta

import discord
from discord import app_commands
from discord.ext import commands


class MemberWelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_welcome_time = {}
        self.db_path = "data/welcome.db"
        self._init_database()

    def _init_database(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS welcome_settings (
            guild_id INTEGER PRIMARY KEY,
            is_enabled INTEGER DEFAULT 0,
            member_increment INTEGER DEFAULT 100
        )
        """)

        conn.commit()
        conn.close()

    def _get_guild_settings(self, guild_id: int) -> tuple:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT is_enabled, member_increment FROM welcome_settings WHERE guild_id = ?",
            (guild_id,)
        )
        result = cursor.fetchone()
        conn.close()

        if result is None:
            return (False, 100)  # デフォルト100人ずつ
        return (bool(result[0]), result[1])

    def _update_guild_settings(self, guild_id: int, is_enabled: bool, member_increment: int = None):
        """Update guild welcome settings"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO welcome_settings (guild_id, is_enabled, member_increment)
            VALUES (?, ?, ?)
            ON CONFLICT(guild_id) DO UPDATE SET
                is_enabled = excluded.is_enabled,
                member_increment = COALESCE(?, welcome_settings.member_increment)
            """,
            (guild_id, is_enabled, member_increment, member_increment)
        )

        conn.commit()
        conn.close()

    @app_commands.command(
        name="welcome",
        description="参加メッセージの設定"
    )
    @app_commands.describe(
        action="on/off - 参加メッセージをON/OFFにします",
        increment="何人ごとにお祝いメッセージを送信するか設定 (デフォルト: 100)"
    )
    async def welcome_command(
        self,
        interaction: discord.Interaction,
        action: str,
        increment: int = None
    ):
        # このあたりは適宜変更してね
        if not interaction.user.guild_permissions.manage_guild:
            await interaction.response.send_message("コマンドを使用するにはサーバーの管理権限が必要だよ", ephemeral=True)
            return

        if action.lower() not in ["on", "off"]:
            await interaction.response.send_message("onまたはoffを指定してね", ephemeral=True)
            return

        is_enabled = action.lower() == "on"

        # OFFの時もincrementが指定されるかもだけどまぁ気になるならいじろう
        if increment and (increment < 5 or increment > 1000):
            await interaction.response.send_message("5～1000人の間で指定してね", ephemeral=True)
            return

        self._update_guild_settings(
            interaction.guild_id, is_enabled, increment)

        settings = self._get_guild_settings(interaction.guild_id)
        if is_enabled:
            await interaction.response.send_message(
                f"参加メッセージをONにしたよ!\n{settings[1]}人ごとにお祝いメッセージを送信します",
                ephemeral=True
            )
        else:
            await interaction.response.send_message("参加メッセージを無効にしたよ!", ephemeral=True)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        settings = self._get_guild_settings(member.guild.id)
        if not settings[0]:
            return

        # 参加マクロ対策
        now = datetime.now()
        last_time = self.last_welcome_time.get(member.guild.id)
        if last_time and now - last_time < timedelta(seconds=3):
            return
        self.last_welcome_time[member.guild.id] = now

        # システムメッセージチャンネル
        channel = None
        for ch in member.guild.channels:
            if isinstance(ch, discord.TextChannel) and ch.is_news():
                channel = ch
                break

        if channel is None:
            # 一般チャンネル
            for ch in member.guild.channels:
                if isinstance(ch, discord.TextChannel) and ch.name in ["general", "一般"]:
                    channel = ch
                    break

        if channel is None:
            return  # チャンネルない場合は無視

        guild = self.bot.get_guild(member.guild.id)

        remainder = len(member.guild.members) % settings[1]  # member_increment
        if remainder == 0:
            message = (
                f"🎉🎉🎉 お祝い 🎉🎉🎉\n"
                f"{member.mention} さん、ようこそ！\n"
                f"{len(guild.members)}人達成！\n"
                f"{guild.name}のメンバーが{len(guild.members)}人になりました！皆さんありがとうございます！"
            )
        else:
            remaining_members = settings[1] - remainder
            message = (
                f"{member.mention} さん、ようこそ！\n"
                f"現在のメンバー数: {len(guild.members)}人\n"
                f"あと {remaining_members} 人で {len(guild.members) + remaining_members}人達成です！"
            )

        await channel.send(message)


async def setup(bot: commands.Bot):
    await bot.add_cog(MemberWelcomeCog(bot))
