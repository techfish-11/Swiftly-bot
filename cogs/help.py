import discord
from discord.ext import commands

class GrowthHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="help", description="Swiftlyのヘルプを表示します。")
    async def growth_help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="成長予測コマンドのヘルプ",
            description="サーバーの成長を予測するためのコマンドの使い方と特徴を説明します。",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="/growth-help",
            value=(
                "サーバーの成長をお好きなモデルで予測するためのコマンドのhelpです。\n"
                "特徴:\n"
                "- 3次多項式回帰や、ARIMA、Prophetを使用できます。\n"
                "- サーバーの目標人数は何日に達成するか大体をAIで予測できます。\n"
            ),
            inline=False
        )

        embed.add_field(
            name="/base64",
            value=(
                "base64のエンコード・デコードできます。\n"
                "特徴:\n"
                "- 荒らし対策機能付き\n"
            ),
            inline=False
        )

        embed.add_field(
            name="/first-comment",
            value=(
                "このチャンネルの最初のメッセージへのリンクを取得します。\n"
                "特徴:\n"
                "- このチャンネルの一番最初のメッセージのリンクを取得できます。\n"
            ),
            inline=False
        )

        embed.add_field(
            name="/wikipedia",
            value=(
                "Wikipediaで検索できます。\n"
                "特徴:\n"
                "- Wikipediaでものを検索できます。\n"
                "- 曖昧なページも検索できます。\n"
                "\n\n"
                "ほかにもあります。/command-listで確認してください。"
            ),
            inline=False
        )


        embed.set_footer(text="Hosted by TechFish_Lab")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(GrowthHelp(bot))