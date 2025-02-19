import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import datetime
from typing import Optional

class DescriptionModal(discord.ui.Modal, title="サーバー説明文の設定"):
    description = discord.ui.TextInput(
        label="サーバーの説明",
        placeholder="あなたのサーバーの説明を入力してください",
        style=discord.TextStyle.paragraph,
        max_length=1000,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        with sqlite3.connect('server_board.db') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE servers SET description = ? WHERE server_id = ?',
                         (str(self.description), interaction.guild.id))
            conn.commit()
        await interaction.response.send_message("サーバーの説明文を更新しました！", ephemeral=True)

class ServerBoard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.setup_database()

    def setup_database(self):
        with sqlite3.connect('server_board.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS servers (
                    server_id INTEGER PRIMARY KEY,
                    server_name TEXT NOT NULL,
                    icon_url TEXT,
                    description TEXT,
                    rank_points INTEGER DEFAULT 0,
                    last_up_time TIMESTAMP,
                    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    @app_commands.command(name="register", description="サーバーを掲示板に登録します")
    @app_commands.checks.has_permissions(administrator=True)
    async def register(self, interaction: discord.Interaction):
        guild = interaction.guild
        
        with sqlite3.connect('server_board.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM servers WHERE server_id = ?', (guild.id,))
            if cursor.fetchone():
                await interaction.response.send_message("このサーバーは既に登録されています。", ephemeral=True)
                return

        embed = discord.Embed(
            title="サーバー掲示板への登録",
            description="以下の情報でサーバーを登録します。よろしければ✅を押してください。\n キャンセルする場合は❌を押してください。",
            color=discord.Color.blue()
        )
        embed.add_field(name="サーバー名", value=guild.name)
        embed.add_field(name="アイコン", value="設定済み" if guild.icon else "未設定")
        embed.set_thumbnail(url=guild.icon.url if guild.icon else "")

        class ConfirmView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=180.0)

            @discord.ui.button(style=discord.ButtonStyle.success, emoji="✅", custom_id="confirm")
            async def confirm(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                with sqlite3.connect('server_board.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO servers (server_id, server_name, icon_url)
                        VALUES (?, ?, ?)
                    ''', (guild.id, guild.name, guild.icon.url if guild.icon else None))
                    conn.commit()
                await button_interaction.response.edit_message(content="サーバーを登録しました！", view=None, embed=None)

            @discord.ui.button(style=discord.ButtonStyle.danger, emoji="✖", custom_id="cancel")
            async def cancel(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                await button_interaction.response.edit_message(content="登録をキャンセルしました。", view=None, embed=None)

        view = ConfirmView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @app_commands.command(name="up", description="サーバーの表示順位を上げます")
    async def up_rank(self, interaction: discord.Interaction):
        with sqlite3.connect('server_board.db') as conn:
            cursor = conn.cursor()
            
            # 最後のup実行時刻を確認
            cursor.execute('SELECT last_up_time FROM servers WHERE server_id = ?', (interaction.guild.id,))
            result = cursor.fetchone()
            
            if not result:
                await interaction.response.send_message("このサーバーは登録されていません。", ephemeral=True)
                return

            last_up_time = result[0]
            current_time = datetime.datetime.now()
            
            if last_up_time:
                last_up = datetime.datetime.fromisoformat(last_up_time)
                if (current_time - last_up).total_seconds() < 7200:  # 2時間
                    remaining_time = last_up + datetime.timedelta(hours=2) - current_time
                    await interaction.response.send_message(
                        f"upコマンドは2時間に1回のみ使用できます。\n残り時間: {str(remaining_time).split('.')[0]}",
                        ephemeral=True
                    )
                    return

            # ポイントを更新
            cursor.execute('''
                UPDATE servers
                SET rank_points = rank_points + 1,
                    last_up_time = ?
                WHERE server_id = ?
            ''', (current_time.isoformat(), interaction.guild.id))
            conn.commit()

            await interaction.response.send_message("サーバーの表示順位を上げました！", ephemeral=False)

    @app_commands.command(name="board-setting", description="サーバーの説明文を設定します")
    @app_commands.checks.has_permissions(administrator=True)
    async def board_setting(self, interaction: discord.Interaction):
        # サーバーが登録されているか確認
        with sqlite3.connect('server_board.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT description FROM servers WHERE server_id = ?', (interaction.guild.id,))
            result = cursor.fetchone()
            
            if not result:
                await interaction.response.send_message("このサーバーは登録されていません。先に/registerコマンドで登録してください。", ephemeral=True)
                return

        # モーダルを表示
        modal = DescriptionModal()
        if result[0]:  # 既存の説明文があれば、それをデフォルト値として設定
            modal.description.default = result[0]
            
        await interaction.response.send_modal(modal)

    @app_commands.command(name="unregister", description="サーバーの登録を削除します")
    @app_commands.checks.has_permissions(administrator=True)
    async def unregister(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="サーバー掲示板からの登録削除",
            description="本当にこのサーバーの登録を削除しますか？\nこの操作は取り消せません。",
            color=discord.Color.red()
        )

        class UnregisterView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=180.0)

            @discord.ui.button(style=discord.ButtonStyle.danger, emoji="✅", custom_id="confirm")
            async def confirm(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                with sqlite3.connect('server_board.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('DELETE FROM servers WHERE server_id = ?', (interaction.guild.id,))
                    if cursor.rowcount > 0:
                        conn.commit()
                        await button_interaction.response.edit_message(content="サーバーの登録を削除しました。", view=None, embed=None)
                    else:
                        await button_interaction.response.edit_message(content="このサーバーは登録されていません。", view=None, embed=None)

            @discord.ui.button(style=discord.ButtonStyle.secondary, emoji="❌", custom_id="cancel")
            async def cancel(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                await button_interaction.response.edit_message(content="登録削除をキャンセルしました。", view=None, embed=None)

        view = UnregisterView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(ServerBoard(bot))