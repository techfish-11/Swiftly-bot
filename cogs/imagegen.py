import discord
from discord.ext import commands
import aiohttp

class ImageGen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="imagegen", description="Generates an image based on the given prompt")
    async def imagegen(self, interaction: discord.Interaction, prompt: str) -> None:
        await interaction.response.defer(thinking=True)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://image-ai.evex.land/?prompt={prompt}") as response:
                if response.status == 200:
                    image_url = str(response.url)
                    embed = discord.Embed(
                        title="Generated Image",
                        description=f"Prompt: {prompt}",
                        color=discord.Color.blue()
                    )
                    embed.set_image(url=image_url)
                    embed.set_footer(text="API Powered by Evex")
                    await interaction.followup.send(embed=embed)
                else:
                    await interaction.followup.send("Failed to generate image. Please try again later.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ImageGen(bot))