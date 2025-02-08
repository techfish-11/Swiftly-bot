import discord
from discord.ext import commands
import random

class LoveCalculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="love-calculator", description="2人のユーザーを選択して愛の相性を計算します")
    async def love_calculator(self, interaction: discord.Interaction, user1: discord.User, user2: discord.User):
        name1 = user1.name
        name2 = user2.name
        id1 = user1.id
        id2 = user2.id
        love_score = self.K7LoveCalc(id1, id2)
        message = self.get_love_message(love_score[0])
        
        embed = discord.Embed(title="💖 Love Calculator 💖", color=discord.Color.pink())
        embed.add_field(name="ユーザー1", value=name1, inline=True)
        embed.add_field(name="ユーザー2", value=name2, inline=True)
        embed.add_field(name=name1+"→"+name2, value=f"{love_score[1]}%", inline=False)
        embed.add_field(name=name2+"→"+name1, value=f"{love_score[2]}%", inline=False)
        embed.add_field(name="総合相性", value=f"{love_score[0]}%", inline=False)
        embed.add_field(name="メッセージ", value=message, inline=False)
        
        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(name="reverse", description="テキストを逆さまにして表示します")
    async def reverse(self, interaction: discord.Interaction, text: str):
        reversed_text = text[::-1]
        await interaction.response.send_message(reversed_text)

    def K7LoveCalc(self, id0: int, id1: int):
        random.seed(id0 + id1)
        user1_to_user2 = random.randint(0, 100)
        user2_to_user1 = random.randint(0, 100)
        love_score = (user1_to_user2 + user2_to_user1) // 2
        return [love_score, user1_to_user2, user2_to_user1]

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