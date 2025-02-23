import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="help", description="Swiftlyのヘルプを表示します。")
    async def growth_help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Swiftlyヘルプ",
            description="Swiftlyのコマンドの使い方と特徴を説明します。",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="/growth, /prophet-growth, /arima-growth",
            value=(
                "サーバーの成長をAIで予測できるコマンドです。\n"
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
                "ほかにもあります。https://sakana11.org/swiftly/commands.html で確認してください。"
            ),
            inline=False
        )

        embed.set_footer(
            text="Hosted by TechFish_Lab")

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
