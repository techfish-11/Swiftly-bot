import discord
from discord.ext import commands
from collections import Counter
import re

class Youyaku(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='youyaku', description='指定したチャンネルのメッセージを要約します。')
    async def youyaku(self, interaction: discord.Interaction, channel: discord.TextChannel, num_messages: int = 100):
        if num_messages > 1000:
            await interaction.response.send_message("num_messagesの上限は1000です。", ephemeral=True)
            return

        await interaction.response.defer(thinking=True)

        try:
            messages = [message async for message in channel.history(limit=num_messages)]
            message_contents = [message.content for message in messages if message.content]

            if not message_contents:
                await interaction.followup.send("要約するメッセージが見つかりませんでした。")
                return

            combined_text = ' '.join(message_contents)
            japanese_stop_words = ["の", "に", "は", "を", "た", "が", "で", "て", "と", "し", "れ", "さ", "ある", "いる", "も", "する", "から", "な", "こと", "として", "い", "や", "れる", "など", "なっ", "ない", "この", "ため", "その", "あっ", "よう", "また", "もの", "という", "あり", "まで", "られ", "なる", "へ", "か", "だ", "これ", "によって", "により", "おり", "より", "による", "ず", "なり", "られる"]
            words = re.findall(r'\b\w+\b', combined_text)
            filtered_words = [w for w in words if w not in japanese_stop_words]
            word_counts = Counter(filtered_words)

            sentences = re.split(r'[。！？.!?]', combined_text)
            def sentence_score(sentence):
                sw = re.findall(r'\b\w+\b', sentence)
                return sum(word_counts.get(w, 0) for w in sw)

            scored = [(s, sentence_score(s)) for s in sentences if s.strip()]
            scored.sort(key=lambda x: x[1], reverse=True)
            top_sentences = [s for s, _ in scored[:5]]
            summary = '。'.join(top_sentences)

            embed = discord.Embed(title=f"直近の{num_messages}件のメッセージの要約", description=summary, color=discord.Color.blue())
            await interaction.followup.send(embed=embed)
        except discord.DiscordException as e:
            await interaction.followup.send(f"Discordでエラーが発生しました: {str(e)}")
        except Exception as e:
            await interaction.followup.send(f"予期しないエラーが発生しました: {str(e)}")

async def setup(bot):
    await bot.add_cog(Youyaku(bot))