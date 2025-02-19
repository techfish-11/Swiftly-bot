import discord
from discord.ext import commands, tasks
import sqlite3
from datetime import datetime, timezone, timedelta

DB_FILE = "registered_channels.db"
JST = timezone(timedelta(hours=9))

class TimeRegister(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.init_db()
        self.check_time.start()

    def init_db(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS channels (
                channel_id INTEGER PRIMARY KEY
            )
        """)
        conn.commit()
        conn.close()

    @discord.app_commands.command(name="register19", description="チャンネルを登録し、19時19分に通知します")
    @discord.app_commands.describe(channel_id="通知対象のチャンネルID")
    async def register19(self, interaction: discord.Interaction, channel_id: int) -> None:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT OR IGNORE INTO channels (channel_id) VALUES (?)", (channel_id,))
            conn.commit()
            await interaction.response.send_message(f"チャンネルID {channel_id} を19時19分時報に登録しました。/register-remove19 で登録を解除できます。")
        except Exception as e:
            await interaction.response.send_message("登録中にエラーが発生しました。")
        finally:
            conn.close()

    @discord.app_commands.command(name="register-remove19", description="登録解除し、19時19分の通知対象から外します")
    @discord.app_commands.describe(channel_id="通知解除するチャンネルID")
    async def unregister19(self, interaction: discord.Interaction, channel_id: int) -> None:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM channels WHERE channel_id = ?", (channel_id,))
            conn.commit()
            if cursor.rowcount:
                await interaction.response.send_message(f"チャンネルID {channel_id} の登録を解除しました。")
            else:
                await interaction.response.send_message(f"チャンネルID {channel_id} は登録されていません。")
        except Exception as e:
            await interaction.response.send_message("登録解除中にエラーが発生しました。")
        finally:
            conn.close()

    @tasks.loop(minutes=1)
    async def check_time(self):
        now = datetime.now(JST)
        if now.hour == 19 and now.minute == 19:
            await self.send_notification()

    async def send_notification(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT channel_id FROM channels")
        channels = cursor.fetchall()
        conn.close()

        for (channel_id,) in channels:
            channel = self.bot.get_channel(channel_id)
            if channel:
                try:
                    await channel.send("19時19分です！1919！")
                except Exception:
                    pass  # Optionally log the error

    @check_time.before_loop
    async def before_check_time(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(TimeRegister(bot))