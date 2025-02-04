import re
from collections import Counter

import discord
from discord.ext import commands


class Youyaku(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="youyaku", description="指定したチャンネルのメッセージを要約します。")
    async def youyaku(self, interaction: discord.Interaction, channel: discord.TextChannel, num_messages: int = 100):
        if num_messages > 1000:
            await interaction.response.send_message("num_messagesの上限は1000です。", ephemeral=True)
            return

        await interaction.response.defer(thinking=True)

        try:
            # Fetch the message history
            messages = []
            async for message in channel.history(limit=num_messages):
                messages.append(message)
            message_contents = [
                message.content for message in messages if message.content]

            if not message_contents:
                await interaction.followup.send("要約するメッセージが見つかりませんでした。")
                return

            # Combine all messages into a single text
            combined_text = " ".join(message_contents)

            # Tokenize the text and remove stop words
            japanese_stop_words = [
                "の", "に", "は", "を", "た", "が", "で", "て", "と", "し", "れ", "さ", "ある", "いる", "も",
                "する", "から", "な", "こと", "として", "い", "や", "れる", "など", "なっ", "ない", "この",
                "ため", "その", "あっ", "よう", "また", "もの", "という", "あり", "まで", "られ", "なる", "へ",
                "か", "だ", "これ", "によって", "により", "おり", "より", "による", "ず", "なり", "られる"
            ]

            words = re.findall(r"\b\w+\b", combined_text)
            filtered_words = [word for word in words if word not in japanese_stop_words]

            # Count the frequency of each word
            word_counts = Counter(filtered_words)

            # Get the most common words
            most_common_words = word_counts.most_common(10)
            summary_list = [f"{word}: {count}" for word, count in most_common_words]
            summary = "\n".join(summary_list)

            # Create an embed with the summary
            embed = discord.Embed(title=f"直近の{num_messages}件のメッセージの要約", description=summary, color=discord.Color.blue())
            await interaction.followup.send(embed=embed)
        except discord.DiscordException as e:
            await interaction.followup.send(f"Discordでエラーが発生しました: {e}")
        except Exception as e:
            await interaction.followup.send(f"予期しないエラーが発生しました: {e}")


async def setup(bot):
    await bot.add_cog(Youyaku(bot))
