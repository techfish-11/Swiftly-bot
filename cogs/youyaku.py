import discord
from discord.ext import commands
from sklearn.feature_extraction.text import TfidfVectorizer
import os

class Youyaku(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='youyaku', description='指定したチャンネルのメッセージを要約します。')
    async def youyaku(self, ctx, channel: discord.TextChannel, num_messages: int = 100):
        await ctx.defer()

        try:
            # Fetch the message history
            messages = await channel.history(limit=num_messages).flatten()
            message_contents = [message.content for message in messages if message.content]

            if not message_contents:
                await ctx.send("No messages found to summarize.")
                return

            # Create the TF-IDF Vectorizer
            vectorizer = TfidfVectorizer(stop_words='english')
            X = vectorizer.fit_transform(message_contents)

            # Get the highest scoring message
            scores = X.sum(axis=1).A1
            top_message_index = scores.argmax()
            summary = message_contents[top_message_index]

            embed = discord.Embed(title=f"Summary of the last {num_messages} messages", description=summary, color=discord.Color.blue())
            await ctx.send(embed=embed)
        except discord.DiscordException as e:
            await ctx.send(f"An error occurred with Discord: {str(e)}")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {str(e)}")

async def setup(bot):
    await bot.add_cog(Youyaku(bot))