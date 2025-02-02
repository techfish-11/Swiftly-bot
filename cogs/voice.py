import discord
from discord.ext import commands
import pyttsx3
import tempfile
import os

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tts_engine = pyttsx3.init()
        
        # Set TTS properties
        self.tts_engine.setProperty('rate', 125)  # setting up new voice rate
        self.tts_engine.setProperty('volume', 1.0)  # setting up volume level between 0 and 1
        voices = self.tts_engine.getProperty('voices')
        self.tts_engine.setProperty('voice', voices[1].id)  # changing index, changes voices. 1 for female

    @discord.app_commands.command(name="join", description="ボイスチャンネルに参加します")
    async def join(self, interaction: discord.Interaction):
        if not interaction.user.voice:
            embed = discord.Embed(
                description="先にボイスチャンネルに参加してください。",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
            return

        voice_channel = interaction.user.voice.channel

        try:
            if interaction.guild.voice_client:
                await interaction.guild.voice_client.move_to(voice_channel)
            else:
                await voice_channel.connect()
            
            embed = discord.Embed(
                description=f"✅ {voice_channel.name} に参加しました。",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = discord.Embed(
                description=f"エラーが発生しました: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)

    @discord.app_commands.command(name="leave", description="ボイスチャンネルから退出します")
    async def leave(self, interaction: discord.Interaction):
        if not interaction.guild.voice_client:
            embed = discord.Embed(
                description="ボイスチャンネルに参加していません。",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
            return

        try:
            await interaction.guild.voice_client.disconnect()
            embed = discord.Embed(
                description="👋 ボイスチャンネルから退出しました。",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = discord.Embed(
                description=f"エラーが発生しました: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)

    @discord.app_commands.command(name="vc-tts", description="メッセージを読み上げます")
    async def vc_tts(self, interaction: discord.Interaction, message: str):
        if not interaction.user.voice:
            embed = discord.Embed(
                description="先にボイスチャンネルに参加してください。",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
            return

        voice_channel = interaction.user.voice.channel

        try:
            if not interaction.guild.voice_client:
                await voice_channel.connect()

            # Generate TTS audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
                self.tts_engine.save_to_file(message, temp_audio_file.name)
                self.tts_engine.runAndWait()
                temp_audio_file.close()

                # Play the audio in the voice channel
                voice_client = interaction.guild.voice_client
                voice_client.play(discord.FFmpegPCMAudio(temp_audio_file.name), after=lambda _: os.remove(temp_audio_file.name))

            embed = discord.Embed(
                description=f"📢 メッセージを読み上げました: {message}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = discord.Embed(
                description=f"エラーが発生しました: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        del before, after  # Unused variables
        voice_client = member.guild.voice_client
        if voice_client:
            if len(voice_client.channel.members) == 1:  # ボットだけが残っている場合
                await voice_client.disconnect()

async def setup(bot):
    await bot.add_cog(Voice(bot))