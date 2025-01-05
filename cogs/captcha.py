import discord
from discord.ext import commands
import aiohttp
import base64
from io import BytesIO

class Captcha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='captcha', description='Generate a CAPTCHA image.')
    @discord.app_commands.describe(difficulty='Difficulty level of the CAPTCHA (1-10)')
    async def captcha(self, ctx: discord.Interaction, difficulty: int = 1) -> None:
        if difficulty < 1 or difficulty > 10:
            await ctx.response.send_message('Difficulty must be between 1 and 10.', ephemeral=True)
            return

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://captcha.evex.land/api/captcha?difficulty={difficulty}') as response:
                if response.status == 200:
                    data = await response.json()
                    image_data = data['image'].split(',')[1]
                    image_bytes = base64.b64decode(image_data)
                    image_file = discord.File(BytesIO(image_bytes), filename='captcha.png')
                    answer = data['answer']
                    embed = discord.Embed(title="CAPTCHA", description=f"Difficulty: {difficulty}", color=discord.Color.blue())
                    embed.set_image(url="attachment://captcha.png")
                    embed.set_footer(text=f"Image provided by https://captcha.evex.land/client/\nAnswer: {answer}")
                    await ctx.response.send_message(embed=embed, file=image_file, ephemeral=True)
                else:
                    await ctx.response.send_message('Failed to retrieve CAPTCHA.', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Captcha(bot))