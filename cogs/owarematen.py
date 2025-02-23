import discord
from discord.ext import commands

servers = {}

class DiscowaremaTen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="owarematen-start-custom", description="終われまテンをカスタムお題で開始します。")
    async def start_custom(self, ctx, theme:str):
        if ctx.guild_id in servers:
            embed = discord.Embed(title="終われまテン", description="V1.0 by K-Nana", color=discord.Color.red())
            embed.add_field(name="他のゲームが進行中です", value="先に/open_answersでゲームを終了してください。", inline=False)
            await ctx.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="終われまテン", description="V1.0 by K-Nana", color=discord.Color.blurple())
            embed.add_field(name="お題", value=theme, inline=False)
            embed.add_field(name="回答方法", value="/answerで回答できます。", inline=False)
            servers[ctx.guild_id] = {"theme": theme, "answers": {}}
            await ctx.response.send_message(embed=embed)

    @discord.app_commands.command(name="owarematen-open-answers", description="全員の回答を開きます。終われまテンの終了コマンドも兼ねています。")
    async def open_answers(self, ctx):
        if ctx.guild_id in servers:
            embed = discord.Embed(title="終われまテン", description="V1.0 by K-Nana", color=discord.Color.green())
            embed.add_field(name="お題", value=servers[ctx.guild_id]["theme"], inline=False)
            if len(servers[ctx.guild_id]["answers"]) == 0:
                embed.add_field(name="おっと。", value="誰も答えていないようです...", inline=True)
            else:
                for name, answer in servers[ctx.guild_id]["answers"].items():
                    embed.add_field(name=name+"の回答", value=answer, inline=True)
            servers.pop(ctx.guild_id)
            await ctx.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="終われまテン", description="V1.0 by K-Nana", color=discord.Color.red())
            embed.add_field(name="ゲームが開始されていません", value="先に/start_customでゲームを開始してください。", inline=False)
            await ctx.response.send_message(embed=embed)

    @discord.app_commands.command(name="owarematen-answer", description="終われまテンに回答します。")
    async def answer(self, ctx, answer:str):
        servers[ctx.guild_id]["answers"][ctx.user.name] = answer
        await ctx.response.send_message(answer+"で回答しました", ephemeral=True)
        await ctx.channel.send(ctx.user.name+"が回答しました（回答者数："+str(len(servers[ctx.guild_id]["answers"]))+"）")


async def setup(bot):
    await bot.add_cog(DiscowaremaTen(bot))