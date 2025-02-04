import discord
from discord.ext import commands

class Sizi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="sizi", description="指定した内容を指定した相手に指示します。")
    async def sizi(self, interaction: discord.Interaction, content: str, target: discord.Member):
        try:
            # Create an embed with the instruction
            embed = discord.Embed(
                title="指示",
                description=f"{interaction.user.mention}が、{target.mention}に「{content}」を指示しました。",
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed)
        except discord.DiscordException as e:
            await interaction.response.send_message(f"Discordでエラーが発生しました: {e}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"予期しないエラーが発生しました: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Sizi(bot))