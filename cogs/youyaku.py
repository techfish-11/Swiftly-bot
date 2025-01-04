import discord
from discord.ext import commands
from sklearn.feature_extraction.text import TfidfVectorizer

class Youyaku(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='youyaku', description='指定したチャンネルのメッセージを要約します。')
    async def youyaku(self, interaction: discord.Interaction, channel: discord.TextChannel, num_messages: int = 100):
        await interaction.response.defer(thinking=True)

        try:
            # Fetch the message history
            messages = [message async for message in channel.history(limit=num_messages)]
            message_contents = [message.content for message in messages if message.content]

            if not message_contents:
                await interaction.followup.send("要約するメッセージが見つかりませんでした。")
                return

            # Create the TF-IDF Vectorizer with Japanese stop words
            japanese_stop_words = ["の", "に", "は", "を", "た", "が", "で", "て", "と", "し", "れ", "さ", "ある", "いる", "も", "する", "から", "な", "こと", "として", "い", "や", "れる", "など", "なっ", "ない", "この", "ため", "その", "あっ", "よう", "また", "もの", "という", "あり", "まで", "られ", "なる", "へ", "か", "だ", "これ", "によって", "により", "おり", "より", "による", "ず", "なり", "られる"]
            vectorizer = TfidfVectorizer(stop_words=japanese_stop_words)
            vectorizer = TfidfVectorizer(stop_words=japanese_stop_words if isinstance(japanese_stop_words, list) else None)

            # Get the highest scoring message
            scores = X.sum(axis=1).A1
            top_message_index = scores.argmax()
            summary = message_contents[top_message_index]

            embed = discord.Embed(title=f"直近の{num_messages}件のメッセージの要約", description=summary, color=discord.Color.blue())
            await interaction.followup.send(embed=embed)
        except discord.DiscordException as e:
            await interaction.followup.send(f"Discordでエラーが発生しました: {str(e)}")
        except Exception as e:
            await interaction.followup.send(f"予期しないエラーが発生しました: {str(e)}")

async def setup(bot):
    await bot.add_cog(Youyaku(bot))