import discord
from discord.ext import commands
import aiohttp
import io

class ImageGen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="imagegen", description="Generates an image based on the given prompt")
    async def imagegen(self, interaction: discord.Interaction, prompt: str) -> None:
        await interaction.response.defer(thinking=True)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://image-ai.evex.land/?prompt={prompt}") as response:
                if response.status == 200:
                    image_data = await response.read()
                    image_file = discord.File(io.BytesIO(image_data), filename="generated_image.png")
                    embed = discord.Embed(
                        title="Generated Image",
                        description=f"Prompt: {prompt}",
                        color=discord.Color.blue()
                    )
                    embed.set_image(url="attachment://generated_image.png")
                    embed.set_footer(text="API Powered by Evex")
                    await interaction.followup.send(embed=embed, file=image_file)
                else:
                    await interaction.followup.send("Failed to generate image. Please try again later.", ephemeral=True)

        @discord.app_commands.command(name="ip", description="Fetches IP information for the given IP address")
        async def ip_info(self, interaction: discord.Interaction, ip_addr: str) -> None:
            await interaction.response.defer(thinking=True)
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://ip.evex.land/{ip_addr}") as response:
                    if response.status == 200:
                        ip_data = await response.json()
                        embed = discord.Embed(
                            title="IP Information",
                            description=f"Information for IP: {ip_addr}",
                            color=discord.Color.green()
                        )
                        embed.set_footer(text="API Powered by Evex")
                        for key, value in ip_data.items():
                            embed.add_field(name=key, value=value, inline=False)
                        await interaction.followup.send(embed=embed)
                    else:
                        await interaction.followup.send("Failed to fetch IP information. Please try again later.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ImageGen(bot))