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
                    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    invite_url TEXT
                )
            ''')
            conn.commit()

    @app_commands.command(name="register", description="サーバーを掲示板に登録します")
    @app_commands.checks.has_permissions(administrator=True)
    async def register(self, interaction: discord.Interaction):
        try:
            # まず応答を遅延させる
            await interaction.response.defer(ephemeral=True)
            
            guild = interaction.guild
            
            # データベース接続のエラーハンドリング
            try:
                with sqlite3.connect('server_board.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('SELECT * FROM servers WHERE server_id = ?', (guild.id,))
                    if cursor.fetchone():
                        await interaction.followup.send("このサーバーは既に登録されています。", ephemeral=True)
                        return
            except sqlite3.Error as e:
                await interaction.followup.send(f"データベースエラーが発生しました。時間をおいて再度お試しください。\nエラー: {str(e)}", ephemeral=True)
                return

            # 招待リンクを作成（システムチャンネルまたは最初の書き込み可能なチャンネルで）
            try:
                invite_channel = guild.system_channel or next((ch for ch in guild.text_channels if ch.permissions_for(guild.me).create_instant_invite), None)
                if not invite_channel:
                    await interaction.followup.send("招待リンクを作成できるチャンネルがありません。ボットの権限を確認してください。", ephemeral=True)
                    return

                try:
                    invite = await invite_channel.create_invite(max_age=0, max_uses=0, reason="サーバー掲示板用の永続的な招待リンク")
                except discord.Forbidden:
                    await interaction.followup.send("招待リンクを作成する権限がありません。ボットに「招待リンクの作成」権限があることを確認してください。", ephemeral=True)
                    return
                except discord.HTTPException as e:
                    await interaction.followup.send(f"招待リンクの作成中にエラーが発生しました。時間をおいて再度お試しください。\nエラー: {str(e)}", ephemeral=True)
                    return

            except Exception as e:
                await interaction.followup.send(f"招待リンク作成時に予期せぬエラーが発生しました。\nエラー: {str(e)}", ephemeral=True)
                return

            embed = discord.Embed(
                title="サーバー掲示板への登録",
                description="以下の情報でサーバーを登録します。よろしければ✅を押してください。\n キャンセルする場合は❌を押してください。",
                color=discord.Color.blue()
            )
            embed.add_field(name="サーバー名", value=guild.name)
            embed.add_field(name="アイコン", value="設定済み" if guild.icon else "未設定")
            embed.add_field(name="招待リンク", value=invite.url, inline=False)
            if guild.icon:
                try:
                    embed.set_thumbnail(url=guild.icon.url)
                except:
                    pass  # アイコンの設定に失敗しても続行

            class ConfirmView(discord.ui.View):
                def __init__(self):
                    super().__init__(timeout=180.0)

                @discord.ui.button(style=discord.ButtonStyle.success, emoji="✅", custom_id="confirm")
                async def confirm(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                    try:
                        await button_interaction.response.defer(ephemeral=True)
                        try:
                            with sqlite3.connect('server_board.db') as conn:
                                cursor = conn.cursor()
                                cursor.execute('''
                                    INSERT INTO servers (server_id, server_name, icon_url, invite_url)
                                    VALUES (?, ?, ?, ?)
                                ''', (guild.id, guild.name, guild.icon.url if guild.icon else None, invite.url))
                                conn.commit()
                        except sqlite3.Error as e:
                            await button_interaction.followup.send(f"データベースエラーが発生しました。時間をおいて再度お試しください。\nエラー: {str(e)}", ephemeral=True)
                            return
                        
                        await button_interaction.followup.send("サーバーを登録しました！", ephemeral=True)
                        try:
                            await button_interaction.message.delete()
                        except:
                            pass  # メッセージの削除に失敗しても無視
                    except Exception as e:
                        await button_interaction.followup.send(f"予期せぬエラーが発生しました。\nエラー: {str(e)}", ephemeral=True)

                @discord.ui.button(style=discord.ButtonStyle.danger, emoji="❌", custom_id="cancel")
                async def cancel(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                    try:
                        await button_interaction.response.defer(ephemeral=True)
                        try:
                            await invite.delete()  # キャンセル時は作成した招待も削除
                        except:
                            pass  # 招待の削除に失敗しても続行
                        
                        await button_interaction.followup.send("登録をキャンセルしました。", ephemeral=True)
                        try:
                            await button_interaction.message.delete()
                        except:
                            pass  # メッセージの削除に失敗しても無視
                    except Exception as e:
                        await button_interaction.followup.send(f"予期せぬエラーが発生しました。\nエラー: {str(e)}", ephemeral=True)

                async def on_timeout(self):
                    try:
                        await invite.delete()  # タイムアウト時は作成した招待も削除
                    except:
                        pass

            view = ConfirmView()
            await interaction.followup.send(embed=embed, view=view, ephemeral=True)

        except Exception as e:
            try:
                await interaction.followup.send(f"予期せぬエラーが発生しました。時間をおいて再度お試しください。\nエラー: {str(e)}", ephemeral=True)
            except:
                # interactionが既に失効している場合は何もしない
                pass

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
                await button_interaction.response.defer(ephemeral=True)
                with sqlite3.connect('server_board.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('DELETE FROM servers WHERE server_id = ?', (interaction.guild.id,))
                    if cursor.rowcount > 0:
                        conn.commit()
                        await button_interaction.followup.send("サーバーの登録を削除しました。", ephemeral=True)
                        await button_interaction.message.delete()
                    else:
                        await button_interaction.followup.send("このサーバーは登録されていません。", ephemeral=True)
                        await button_interaction.message.delete()

            @discord.ui.button(style=discord.ButtonStyle.secondary, emoji="❌", custom_id="cancel")
            async def cancel(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                await button_interaction.response.defer(ephemeral=True)
                await button_interaction.followup.send("登録削除をキャンセルしました。", ephemeral=True)
                await button_interaction.message.delete()

        view = UnregisterView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(ServerBoard(bot))