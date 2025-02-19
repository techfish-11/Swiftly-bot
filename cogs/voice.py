import asyncio
import os
import re
import tempfile

import edge_tts
import discord
from discord.ext import commands

VOICE = "ja-JP-NanamiNeural"  # Predefined voice


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_clients = {}  # Track voice clients per guild and channel
        self.locks = {}  # Locks for each guild to prevent race conditions
        self.monitored_channels = {}  # Track monitored text channels per guild

    def sanitize_message(self, text: str) -> str:
        # Replace any URL with "URL省略"
        text = re.sub(r'http[s]?://\S+', 'URL省略', text)
        # Replace any user mention with "メンション省略"
        text = re.sub(r'<@!?[0-9]+>', 'メンション省略', text)
        # Replace role and channel mentions if needed
        text = re.sub(r'<@&[0-9]+>', 'メンション省略', text)
        text = re.sub(r'<#[0-9]+>', 'メンション省略', text)
        return text

    @discord.app_commands.command(name="join", description="ボイスチャンネルに参加します")
    async def join(self, interaction: discord.Interaction):
        member = interaction.guild.get_member(interaction.user.id)
        if not member or not member.voice:
            embed = discord.Embed(
                description="先にボイスチャンネルに参加してください。",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
            return

        voice_channel = member.voice.channel
        guild_id = interaction.guild.id
        channel_id = voice_channel.id

        try:
            if guild_id in self.voice_clients and channel_id in self.voice_clients[guild_id]:
                await self.voice_clients[guild_id][channel_id].move_to(voice_channel)
            else:
                voice_client = await voice_channel.connect()
                if guild_id not in self.voice_clients:
                    self.voice_clients[guild_id] = {}
                self.voice_clients[guild_id][channel_id] = voice_client

            # Mute the bot
            voice_client = self.voice_clients[guild_id][channel_id]
            await voice_client.guild.change_voice_state(channel=voice_client.channel, self_deaf=True)

            # Monitor the text channel where the join command was issued
            self.monitored_channels[guild_id] = interaction.channel.id

            embed = discord.Embed(
                description=f"✅ {voice_channel.name} に参加しました。",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = discord.Embed(
                description=f"エラーが発生しました: {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)

    @discord.app_commands.command(name="leave", description="ボイスチャンネルから退出します")
    async def leave(self, interaction: discord.Interaction):
        member = interaction.guild.get_member(interaction.user.id)
        if not member or not member.voice:
            embed = discord.Embed(
                description="ボイスチャンネルに参加していません。",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
            return

        guild_id = interaction.guild.id
        voice_channel = member.voice.channel
        channel_id = voice_channel.id

        if guild_id not in self.voice_clients or channel_id not in self.voice_clients[guild_id]:
            embed = discord.Embed(
                description="ボイスチャンネルに参加していません。",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
            return

        try:
            await self.voice_clients[guild_id][channel_id].disconnect()
            del self.voice_clients[guild_id][channel_id]
            if not self.voice_clients[guild_id]:
                del self.voice_clients[guild_id]

            # Stop monitoring the text channel
            if guild_id in self.monitored_channels:
                del self.monitored_channels[guild_id]

            embed = discord.Embed(
                description="👋 ボイスチャンネルから退出しました。",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = discord.Embed(
                description=f"エラーが発生しました: {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)

    @discord.app_commands.command(name="vc-tts", description="メッセージを読み上げます")
    async def vc_tts(self, interaction: discord.Interaction, message: str):
        member = interaction.guild.get_member(interaction.user.id)
        if not member or not member.voice:
            embed = discord.Embed(
                description="先にボイスチャンネルに参加してください。",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
            return

        voice_channel = member.voice.channel
        guild_id = interaction.guild.id
        channel_id = voice_channel.id

        if guild_id not in self.voice_clients or channel_id not in self.voice_clients[guild_id]:
            embed = discord.Embed(
                description="ボイスチャンネルに参加していません。",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
            return

        # Sanitize the message to replace URLs and mentions
        sanitized_message = self.sanitize_message(message)

        if guild_id not in self.locks:
            self.locks[guild_id] = asyncio.Lock()

        async with self.locks[guild_id]:
            try:
                voice_client = self.voice_clients[guild_id][channel_id]

                # Generate TTS audio using edge_tts
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
                    temp_filename = temp_audio_file.name

                tts = edge_tts.Communicate(sanitized_message, VOICE)
                await tts.save(temp_filename)

                # Stop current playback if any, then play new audio
                if voice_client.is_playing():
                    voice_client.stop()

                voice_client.play(
                    discord.FFmpegPCMAudio(temp_filename),
                    after=lambda e: os.remove(temp_filename) if os.path.exists(temp_filename) else None
                )

                embed = discord.Embed(
                    description=f"📢 メッセージを読み上げました: {sanitized_message}",
                    color=discord.Color.green()
                )
                await interaction.response.send_message(embed=embed, ephemeral=False)
            except Exception as e:
                embed = discord.Embed(
                    description=f"エラーが発生しました: {e}",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=False)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        voice_client = member.guild.voice_client
        if voice_client:
            if len(voice_client.channel.members) == 1:  # ボットだけが残っている場合
                await voice_client.disconnect()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        guild_id = message.guild.id
        if guild_id in self.monitored_channels and message.channel.id == self.monitored_channels[guild_id]:
            if not message.author.voice:
                return
            voice_channel = message.author.voice.channel
            channel_id = voice_channel.id

            if guild_id in self.voice_clients and channel_id in self.voice_clients[guild_id]:
                voice_client = self.voice_clients[guild_id][channel_id]

                if guild_id not in self.locks:
                    self.locks[guild_id] = asyncio.Lock()

                # Sanitize the message to replace URLs and mentions
                sanitized_message = self.sanitize_message(message.content)

                async with self.locks[guild_id]:
                    try:
                        # Generate TTS audio using edge_tts
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
                            temp_filename = temp_audio_file.name

                        tts = edge_tts.Communicate(sanitized_message, VOICE)
                        await tts.save(temp_filename)

                        # Stop current playback if any, then play new audio
                        if voice_client.is_playing():
                            voice_client.stop()

                        voice_client.play(
                            discord.FFmpegPCMAudio(temp_filename),
                            after=lambda e: os.remove(temp_filename) if os.path.exists(temp_filename) else None
                        )
                    except Exception as e:
                        print(f"エラーが発生しました: {e}")


async def setup(bot):
    await bot.add_cog(Voice(bot))
