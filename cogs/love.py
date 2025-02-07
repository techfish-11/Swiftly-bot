import discord
from discord.ext import commands

class LoveCalculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="love-calculator", description="2人のユーザーを選択して愛の相性を計算します")
    async def love_calculator(self, interaction: discord.Interaction, user1: discord.User, user2: discord.User):
        name1 = user1.name
        name2 = user2.name
        love_score = self.calculate_love_score(name1, name2)
        message = self.get_love_message(love_score)
        
        embed = discord.Embed(title="💖 Love Calculator 💖", color=discord.Color.pink())
        embed.add_field(name="ユーザー1", value=name1, inline=True)
        embed.add_field(name="ユーザー2", value=name2, inline=True)
        embed.add_field(name="愛の相性", value=f"{love_score}%", inline=False)
        embed.add_field(name="メッセージ", value=message, inline=False)
        
        await interaction.response.send_message(embed=embed)

    def calculate_love_score(self, name1, name2):
        combined_names = name1 + name2
        total_ascii_value = sum(ord(char) for char in combined_names)
        love_score = total_ascii_value % 101  # Ensure the score is between 0 and 100
        return love_score

    def get_love_message(self, score):
        if score > 80:
            return "素晴らしい相性です！💞"
        elif score > 60:
            return "とても良い相性です！😊"
        elif score > 40:
            return "まあまあの相性です。🙂"
        elif score > 20:
            return "ちょっと微妙かも...😕"
        else:
            return "残念ながら、相性はあまり良くないようです。😢"

async def setup(bot):
    await bot.add_cog(LoveCalculator(bot))