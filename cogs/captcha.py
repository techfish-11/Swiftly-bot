import base64
from io import BytesIO

import aiohttp
import discord
from discord.ext import commands


class Captcha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()  # セッションをクラスレベルで作成

    @discord.app_commands.command(name="captcha", description="CAPTCHA imageを生成します")
    @discord.app_commands.describe(difficulty="Difficulty level of the CAPTCHA (1-10)")
    async def captcha(self, ctx: discord.Interaction, difficulty: int = 1) -> None:
        if difficulty < 1 or difficulty > 10:
            await ctx.response.send_message("Difficulty must be between 1 and 10.", ephemeral=True)
            return

        await ctx.response.defer(thinking=True)  # thinking=Trueを追加

        try:
            async with self.session.get(f"https://captcha.evex.land/api/captcha?difficulty={difficulty}") as response:
                if response.status == 200:
                    data = await response.json()
                    image_data = data["image"].split(",")[1]
                    image_bytes = base64.b64decode(image_data)
                    image_file = discord.File(BytesIO(image_bytes), filename="captcha.png")
                    answer = data["answer"]
                    embed = discord.Embed(title="CAPTCHA", description=f"Difficulty: {difficulty}", color=discord.Color.blue())
                    embed.set_image(url="attachment://captcha.png")
                    embed.set_footer(text=f"Image provided by https://captcha.evex.land/client/\nAnswer: {answer}")
                    await ctx.followup.send(embed=embed, file=image_file)
                else:
                    await ctx.followup.send("Failed to retrieve CAPTCHA.", ephemeral=True)
        except aiohttp.ClientError as e:
            await ctx.followup.send(f"HTTP error occurred: {e}", ephemeral=True)
        except Exception as e:
            await ctx.followup.send(f"An unexpected error occurred: {e}", ephemeral=True)

    async def cog_unload(self):
        self.bot.loop.create_task(self.session.close())  # セッションをクローズ


async def setup(bot):
    await bot.add_cog(Captcha(bot))
