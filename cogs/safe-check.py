import discord
from discord.ext import commands
import re

class SafeCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.discord_invite_pattern = re.compile(r'discord\.gg/\w+|discord\.com/invite/\w+')
        self.AUTHORIZED_USER_ID = 1241397634095120438

    async def is_authorized(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.AUTHORIZED_USER_ID

    @discord.app_commands.command(name="blacklist-add", description="サーバーIDをブラックリストに追加します")
    async def blacklist_add(self, interaction: discord.Interaction, server_id: str):
        if not await self.is_authorized(interaction):
            await interaction.response.send_message("このコマンドを使用する権限がありません。", ephemeral=True)
            return

        try:
            with open('blacklist.txt', 'r') as f:
                blacklist = [line.strip() for line in f.readlines()]
            
            if server_id in blacklist:
                await interaction.response.send_message("このサーバーIDは既にブラックリストに登録されています。", ephemeral=True)
                return

            with open('blacklist.txt', 'a') as f:
                f.write(f"{server_id}\n")
            
            await interaction.response.send_message(f"サーバーID: {server_id} をブラックリストに追加しました。", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"エラーが発生しました: {str(e)}", ephemeral=True)

    @discord.app_commands.command(name="blacklist-remove", description="サーバーIDをブラックリストから削除します")
    async def blacklist_remove(self, interaction: discord.Interaction, server_id: str):
        if not await self.is_authorized(interaction):
            await interaction.response.send_message("このコマンドを使用する権限がありません。", ephemeral=True)
            return

        try:
            with open('blacklist.txt', 'r') as f:
                blacklist = [line.strip() for line in f.readlines()]
            
            if server_id not in blacklist:
                await interaction.response.send_message("指定されたサーバーIDはブラックリストに存在しません。", ephemeral=True)
                return

            blacklist.remove(server_id)
            with open('blacklist.txt', 'w') as f:
                f.write('\n'.join(blacklist) + '\n' if blacklist else '')

            await interaction.response.send_message(f"サーバーID: {server_id} をブラックリストから削除しました。", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"エラーが発生しました: {str(e)}", ephemeral=True)

    @discord.app_commands.command(name="blacklist-search", description="サーバーIDがブラックリストに含まれているか確認します")
    async def blacklist_search(self, interaction: discord.Interaction, server_id: str):
        if not await self.is_authorized(interaction):
            await interaction.response.send_message("このコマンドを使用する権限がありません。", ephemeral=True)
            return

        try:
            with open('blacklist.txt', 'r') as f:
                blacklist = [line.strip() for line in f.readlines()]
            
            is_blacklisted = server_id in blacklist
            await interaction.response.send_message(
                f"サーバーID: {server_id} は{'ブラックリストに登録されています' if is_blacklisted else 'ブラックリストに登録されていません'}",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(f"エラーが発生しました: {str(e)}", ephemeral=True)

    @discord.app_commands.command(name="blacklist-list", description="ブラックリストに登録されているサーバーID一覧を表示します")
    async def blacklist_list(self, interaction: discord.Interaction):
        if not await self.is_authorized(interaction):
            await interaction.response.send_message("このコマンドを使用する権限がありません。", ephemeral=True)
            return

        try:
            with open('blacklist.txt', 'r') as f:
                blacklist = [line.strip() for line in f.readlines()]
            
            if not blacklist:
                await interaction.response.send_message("ブラックリストは空です。", ephemeral=True)
                return

            embed = discord.Embed(
                title="ブラックリスト一覧",
                description="\n".join(blacklist),
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"エラーが発生しました: {str(e)}", ephemeral=True)
            
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        # メッセージ内のDiscordリンクを検索
        invites = self.discord_invite_pattern.finditer(message.content)
        for invite in invites:
            invite_link = invite.group()
            
            # invite_linkからコードだけを抽出
            invite_code = invite_link.split('/')[-1]
            
            # サーバーIDを取得
            guild_id = await self.get_invite_info(invite_code)
            
            if guild_id:
                # ブラックリストを読み込む
                try:
                    with open('blacklist.txt', 'r') as f:
                        blacklist = [line.strip() for line in f.readlines()]
                    
                    # サーバーIDがブラックリストにあるかチェック
                    if str(guild_id) in blacklist:
                        await message.add_reaction('❌')
                    else:
                        await message.add_reaction('✅')
                except FileNotFoundError:
                    # blacklist.txtが存在しない場合は作成
                    open('blacklist.txt', 'w').close()
                    await message.add_reaction('✅')

async def setup(bot):
    await bot.add_cog(SafeCheck(bot))