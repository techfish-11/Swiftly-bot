import discord
from discord.ext import commands
import aiohttp

class Yen5000(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="5000", description="5000兆円ジェネレーター")
    async def yen5000(self, interaction: discord.Interaction, top: str, bottom: str) -> None:
        url = f"https://gsapi.cbrx.io/image?top={top}&bottom={bottom}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    await interaction.response.send_message("画像の生成に失敗しました。", ephemeral=True)
                    return
                
                image_data = await response.read()
                file = discord.File(fp=io.BytesIO(image_data), filename="5000yen.jpeg")

                embed = discord.Embed(
                    title="5000兆円ジェネレーター",
                    description="生成された画像はこちらです。",
                    color=discord.Color.green()
                )
                embed.set_image(url="attachment://5000yen.jpeg")

                await interaction.response.send_message(embed=embed, file=file)

async def setup(bot):
    await bot.add_cog(Yen5000(bot))