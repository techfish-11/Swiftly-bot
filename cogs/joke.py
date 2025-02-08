import discord
from discord.ext import commands
import random

class LoveCalculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="love-calculator", description="2人のユーザーを選択して愛の相性を計算します")
    async def love_calculator(self, interaction: discord.Interaction, user1: discord.User, user2: discord.User):
        if user1 == user2:
            embed = discord.Embed(title="💖 Love Calculator 💖", color=discord.Color.pink())
            embed.add_field(name="メッセージ", value="1人目と2人目で同じユーザーが選択されています。", inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            name1 = user1.name
            name2 = user2.name
            love_score = self.K7LoveCalc(name1, name2)
            message = self.get_love_message(love_score[0], love_score[1], love_score[2])
            embed = discord.Embed(title="💖 Love Calculator 💖", color=discord.Color.pink())
            #embed.add_field(name="ユーザー1", value=name1, inline=True)
            #embed.add_field(name="ユーザー2", value=name2, inline=True)
            embed.add_field(name=name1+"→"+name2, value=f"好感度：{love_score[1]}% 性欲：{love_score[3]}", inline=False)
            embed.add_field(name=name2+"→"+name1, value=f"好感度：{love_score[2]}% 性欲：{love_score[4]}", inline=False)
            embed.add_field(name="総合相性（好感度平均）", value=f"{love_score[0]}%", inline=False)
            embed.add_field(name="メッセージ", value=message, inline=False)
            await interaction.response.send_message(embed=embed)
        
    def K7LoveCalc(self, name1: str, name2: str):
        if name1 > name2:
            combined_names = name1 + name2
        else:
            combined_names = name2 + name1
        random.seed(combined_names)
        user1_to_user2_friend = random.randint(0, 100)
        user2_to_user1_friend = random.randint(0, 100)
        user1_to_user2_sex = random.randint(0, 100)
        user2_to_user1_sex = random.randint(0, 100)
        love_score = (user1_to_user2_friend + user2_to_user1_friend) // 2
        if name1 > name2:
            return [love_score, user1_to_user2_friend, user2_to_user1_friend, user1_to_user2_sex, user2_to_user1_sex]
        else:
            return [love_score, user2_to_user1_friend, user1_to_user2_friend, user2_to_user1_sex, user1_to_user2_sex]

    def get_love_message(self, score, user1_to_user2, user2_to_user1):
        if abs(user1_to_user2 - user2_to_user1) > 30:
            return "片思いの可能性があります。💔"
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
