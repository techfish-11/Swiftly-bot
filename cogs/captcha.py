import base64
from io import BytesIO

import aiohttp
import discord
from discord.ext import commands


class Captcha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @discord.app_commands.command(name="captcha", description="CAPTCHA画像を生成し、解答を検証します")
    @discord.app_commands.describe(difficulty="CAPTCHAの難易度 (1-10)")
    async def captcha(self, ctx: discord.Interaction, difficulty: int = 1) -> None:
        if difficulty < 1 or difficulty > 10:
            await ctx.response.send_message("難易度は1から10の間で指定してください。", ephemeral=True)
            return

        await ctx.response.defer(thinking=True)

        try:
            async with self.session.get(f"https://captcha.evex.land/api/captcha?difficulty={difficulty}") as response:
                if response.status == 200:
                    data = await response.json()
                    image_data = data["image"].split(",")[1]
                    image_bytes = base64.b64decode(image_data)
                    image_file = discord.File(BytesIO(image_bytes), filename="captcha.png")
                    answer = data["answer"]
                    
                    embed = discord.Embed(
                        title="CAPTCHA チャレンジ", 
                        description=f"難易度: {difficulty}\n\n画像に表示されている文字を入力してください。\n制限時間: 30秒", 
                        color=discord.Color.blue()
                    )
                    embed.set_image(url="attachment://captcha.png")
                    
                    await ctx.followup.send(embed=embed, file=image_file)
                    
                    try:
                        def check(m):
                            return m.author == ctx.user and m.channel == ctx.channel
                        
                        response_message = await self.bot.wait_for('message', timeout=30.0, check=check)
                        
                        if response_message.content.lower() == answer.lower():
                            await ctx.followup.send("✅ 正解です！CAPTCHAの認証に成功しました。", ephemeral=True)
                        else:
                            await ctx.followup.send(f"❌ 不正解です。正解は `{answer}` でした。", ephemeral=True)
                    
                    except TimeoutError:
                        await ctx.followup.send("⏰ 時間切れです。もう一度試してください。", ephemeral=True)
                
                else:
                    await ctx.followup.send("CAPTCHAの取得に失敗しました。", ephemeral=True)
        
        except aiohttp.ClientError as e:
            await ctx.followup.send(f"HTTP エラーが発生しました: {e}", ephemeral=True)
        except Exception as e:
            await ctx.followup.send(f"予期せぬエラーが発生しました: {e}", ephemeral=True)

    async def cog_unload(self):
        await self.session.close()


async def setup(bot):
    await bot.add_cog(Captcha(bot))
