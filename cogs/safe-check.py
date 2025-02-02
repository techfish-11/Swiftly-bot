import discord
from discord.ext import commands
import re

class SafeCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.discord_invite_pattern = re.compile(r'discord\.gg/\w+|discord\.com/invite/\w+')

    async def get_invite_info(self, invite_code):
        try:
            invite = await self.bot.fetch_invite(invite_code)
            return invite.guild.id if invite.guild else None
        except:
            return None

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