import discord
from discord.ext import commands
import random
import math
import time
import asyncio

prog_langs = ["C++", "Rust", "Python", "JavaScript", "Go", "Java", "TypeScript", "Swift", "Kotlin", "PHP", "Ruby"]
nice_lang = {"C++": "Rust", "Rust": "Python", "Python": "JavaScript", "JavaScript": "Go", "Go": "Java", "Java": "TypeScript", "TypeScript": "Swift", "Swift": "Kotlin", "Kotlin": "PHP", "PHP": "Ruby", "Ruby": "C++"}
bad_lang = {"Rust": "C++", "Python": "Rust", "JavaScript": "Python", "Go": "JavaScript", "Java": "Go", "TypeScript": "Java", "Swift": "TypeScript", "Kotlin": "Swift", "PHP": "Kotlin", "Ruby": "PHP", "C++": "Ruby"}

class Versus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="fantasy-status", description="特定の人の装備品、攻撃力、守備力、体力を表示する")
    async def fantasy_status(self, interaction: discord.Interaction, user: discord.User):
        name = user.name
        stats = self.K7StatsCalc(name)
        embed = discord.Embed(title="⚔ 異世界ステータスジェネレーター ⚔", color=discord.Color.blue())
        embed.add_field(name="名前", value=name, inline=False)
        embed.add_field(name="装備", value=stats[0], inline=True)
        embed.add_field(name="攻撃力", value=stats[1], inline=True)
        embed.add_field(name="守備力", value=stats[2], inline=True)
        embed.add_field(name="最大HP", value=stats[3], inline=True)
        embed.add_field(name="相性の良い言語（攻撃力 x1.2）", value=nice_lang[stats[0]], inline=True)
        embed.add_field(name="相性の悪い言語（攻撃力 x0.87）", value=bad_lang[stats[0]], inline=True)
        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(name="versus", description="fantasy-statusのステータスをもとに対戦させます。ステータスは固定ですがそれ以外はランダム。")
    async def versus(self, interaction: discord.Interaction, user1: discord.User, user2: discord.User):
        random.seed()
        if user1 == user2:
            embed = discord.Embed(title="⚔ Versus ⚔", color=discord.Color.dark_red())
            embed.add_field(name="メッセージ", value="1人目と2人目で同じユーザーが選択されています。", inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            name1 = user1.name
            name2 = user2.name
            stats1 = self.K7StatsCalc(name1)
            stats2 = self.K7StatsCalc(name2)
            hp1 = stats1[3]
            hp2 = stats2[3]
            embed = discord.Embed(title="⚔ Versus ⚔", color=discord.Color.dark_red())
            turn = random.randint(0,1)
            message = await interaction.response.send_message(embed=embed, wait=True)
            for i in range(20):
                crit = False
                crit_chance = 0.1
                if turn:
                    turn_atk = stats1[1]
                    turn_def = stats2[2]
                    if nice_lang[stats1[0]] == stats2[0]:
                        crit_chance = 0.2
                        turn_atk *= 1.2
                    elif bad_lang[stats1[0]] == stats2[0]:
                        crit_chance = 0.05
                        turn_atk *= 0.87
                    if random.random() <= crit_chance:
                        turn_atk *= 2
                        turn_def = 0
                        crit = True
                    damage = math.floor(max(0, turn_atk*(1-(turn_def/100))))
                    hp2 -= damage
                    if crit:
                        embed.add_field(name=name1+"のターン", value=f"クリティカルヒット！{name2}に{damage}のダメージ！\n残りHP：{hp2}", inline=False)
                    else:
                        embed.add_field(name=name1+"のターン", value=f"{name2}に{damage}のダメージ！\n残りHP：{hp2}", inline=False)
                    if hp2 <= 0:
                        embed.add_field(name=name1+"の勝利！", value=f"{name1}は{hp1}の体力を残して勝利した！", inline=False)
                        break
                else:
                    turn_atk = stats2[1]
                    crit_chance = 0.1
                    turn_def = stats1[2]
                    if nice_lang[stats2[0]] == stats1[0]:
                        crit_chance = 0.2
                        turn_atk *= 1.2
                    elif bad_lang[stats2[0]] == stats1[0]:
                        crit_chance = 0.05
                        turn_atk *= 0.87
                    if random.random() <= crit_chance:
                        turn_atk *= 2
                        turn_def = 0
                        crit = True
                    damage = math.floor(max(0, turn_atk*(1-(turn_def/100))))
                    hp1 -= damage
                    if crit:
                        embed.add_field(name=name2+"のターン", value=f"クリティカルヒット！{name1}に{damage}のダメージ！\n残りHP：{hp1}", inline=False)
                    else:
                        embed.add_field(name=name2+"のターン", value=f"{name1}に{damage}のダメージ！\n残りHP：{hp1}", inline=False)
                    if hp1 <= 0:
                        embed.add_field(name=name2+"の勝利！", value=f"{name2}は{hp2}の体力を残して勝利した！", inline=False)
                        break
                turn = not turn
                await message.edit(embed=embed)
                await asyncio.sleep(random.uniform(0.6, 7))
            if hp1 > 0 and hp2 > 0:
                embed.add_field(name="引き分け", value=f"10ターン以内に戦いが終わらなかった。\n{name1}の体力：{hp1}\n{name2}の体力：{hp2}", inline=False)
            await message.edit(embed=embed)

    def K7StatsCalc(self, name: str):
        random.seed(name)
        weapon = random.choice(prog_langs)
        attack = random.randint(0, 100)
        defence = random.randint(0, 100)
        hp = random.randint(attack+defence, 300)
        return [weapon, attack, defence, hp]

async def setup(bot):
    await bot.add_cog(Versus(bot))