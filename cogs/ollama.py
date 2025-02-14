import discord
from discord.ext import commands
import aiohttp

API_SERVER_URL = "http://192.168.1.7:11434/api/chat"

class OllamaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='llm', description='Send a prompt to the LLM')
    async def llm(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer(thinking=True)
        headers = {"Content-Type": "application/json"}
        json = {
            "model": "llama3.2",
            "stream": False,
            "messages": [{
                "role": "user",
                "content": prompt,
            }]
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(API_SERVER_URL, headers=headers, json=json) as response:
                    response.raise_for_status()
                    data = await response.json()
        except aiohttp.ClientError as e:
            await interaction.followup.send(f"HTTP error occurred: {e}")
            return
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {e}")
            return

        embed = discord.Embed(title="LLM Response", description=data.get('text', 'No response text'), color=discord.Color.blue())
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(OllamaCog(bot))