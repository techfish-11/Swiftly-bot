import discord
from discord.ext import commands
from discord.ui import View, Button
from datetime import datetime, timezone, timedelta
import sqlite3

JST = timezone(timedelta(hours=9))
DB_PATH = "anticheat.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS enabled_servers (guild_id INTEGER PRIMARY KEY)"
    )
    conn.commit()
    conn.close()

init_db()

def is_anticheat_enabled(guild_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM enabled_servers WHERE guild_id = ?", (guild_id,))
    result = c.fetchone()
    conn.close()
    return result is not None

def enable_anticheat(guild_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO enabled_servers (guild_id) VALUES (?)", (guild_id,))
    conn.commit()
    conn.close()

def disable_anticheat(guild_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM enabled_servers WHERE guild_id = ?", (guild_id,))
    conn.commit()
    conn.close()

class ConfirmEnableView(View):
    def __init__(self, guild_id: int):
        super().__init__(timeout=60)  # expires after 60 seconds
        self.guild_id = guild_id

    @discord.ui.button(label="登録", style=discord.ButtonStyle.green, custom_id="confirm_enable")
    async def confirm(self, button: Button, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        try:
            guild = interaction.guild
            if guild is None:
                await interaction.followup.send("このボタンはサーバー内でのみ使用できます。", ephemeral=True)
                self.stop()
                return

            if not interaction.channel.permissions_for(guild.me).manage_messages:
                await interaction.followup.send("Botにメッセージ削除の権限がありません。登録できません。", ephemeral=True)
                self.stop()
                return

            if is_anticheat_enabled(self.guild_id):
                await interaction.followup.send("すでに有効です。", ephemeral=True)
                self.stop()
                return

            enable_anticheat(self.guild_id)
            await interaction.followup.edit_message(
                content="荒らし対策を有効にしました。",
                embed=None,
                view=None
            )
            self.stop()
        except Exception as e:
            await interaction.followup.send(f"インタラクションに失敗しました: {str(e)}", ephemeral=True)
            self.stop()

class IconCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="antiraid_enable", description="荒らし対策を有効にします")
    async def anticheat_enable(self, interaction: discord.Interaction):
        guild = interaction.guild
        if guild is None:
            embed = discord.Embed(
                title="エラー",
                description="このコマンドはサーバー内でのみ使用できます。",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # 管理者権限のチェック
        if not interaction.user.guild_permissions.administrator:
            embed = discord.Embed(
                title="エラー",
                description="このコマンドはサーバーの管理者のみ実行できます。",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if is_anticheat_enabled(guild.id):
            embed = discord.Embed(
                title="情報",
                description="荒らし対策は既に有効です。",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed = discord.Embed(
            title="説明",
            description=("この機能は、デフォルトアバターかつ本日作成されたアカウントによる"
                         "メッセージ送信を制限することで、荒らし対策をします。\n"
                         "登録ボタンを押すことで、荒らし対策を有効にします。"),
            color=discord.Color.blue()
        )
        view = ConfirmEnableView(guild.id)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.app_commands.command(name="antiraid_disable", description="荒らし対策を無効にします")
    async def anticheat_disable(self, interaction: discord.Interaction):
        guild = interaction.guild
        if guild is None:
            embed = discord.Embed(
                title="エラー",
                description="このコマンドはサーバー内でのみ使用できます。",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # 管理者権限のチェック
        if not interaction.user.guild_permissions.administrator:
            embed = discord.Embed(
                title="エラー",
                description="このコマンドはサーバーの管理者のみ実行できます。",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if not is_anticheat_enabled(guild.id):
            embed = discord.Embed(
                title="情報",
                description="荒らし対策は既に無効です。",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        disable_anticheat(guild.id)
        embed = discord.Embed(
            title="完了",
            description="荒らし対策を無効にしました。",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.guild and is_anticheat_enabled(message.guild.id):
            user = message.author

            # デフォルトアバターのチェック
            is_default_avatar = user.avatar is None

            # アカウント作成日が今日かどうかのチェック
            created_at_utc = user.created_at.replace(tzinfo=timezone.utc)
            is_new_account = created_at_utc.date() == datetime.now(timezone.utc).date()

            if is_default_avatar and is_new_account:
                await message.delete()
                embed = discord.Embed(
                    title="警告",
                    description=f"{user.mention}、デフォルトのアバターまたは本日作成されたアカウントではメッセージを送信できません。",
                    color=discord.Color.red()
                )
                warning_message = await message.channel.send(embed=embed)
                await warning_message.delete(delay=5)

async def setup(bot):
    await bot.add_cog(IconCheck(bot))
