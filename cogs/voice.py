import discord
from discord.ext import commands

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="join", description="ボイスチャンネルに参加します")
    async def join(self, interaction: discord.Interaction):
        # Check if the user is in a voice channel
        if not interaction.user.voice:
            await interaction.response.send_message("先にボイスチャンネルに参加してください。", ephemeral=False)
            return

        voice_channel = interaction.user.voice.channel

        try:
            # Check if bot is already in a voice channel in this guild
            if interaction.guild.voice_client:
                await interaction.guild.voice_client.move_to(voice_channel)
            else:
                await voice_channel.connect()
            
            await interaction.response.send_message(f"✅ {voice_channel.name} に参加しました。", ephemeral=False)
        except Exception as e:
            await interaction.response.send_message(f"エラーが発生しました: {str(e)}", ephemeral=False)

    @discord.app_commands.command(name="leave", description="ボイスチャンネルから退出します")
    async def leave(self, interaction: discord.Interaction):
        # Check if bot is in a voice channel
        if not interaction.guild.voice_client:
            await interaction.response.send_message("ボイスチャンネルに参加していません。", ephemeral=False)
            return

        try:
            await interaction.guild.voice_client.disconnect()
            await interaction.response.send_message("👋 ボイスチャンネルから退出しました。", ephemeral=False)
        except Exception as e:
            await interaction.response.send_message(f"エラーが発生しました: {str(e)}", ephemeral=False)

async def setup(bot):
    await bot.add_cog(Voice(bot))