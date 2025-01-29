import discord
from discord.ext import commands

class GrowthHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.Command(name="growth-help", description="成長予測コマンドのヘルプを表示します。")
    async def growth_help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="成長予測コマンドのヘルプ",
            description="サーバーの成長を予測するためのコマンドの使い方と特徴を説明します。",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="/growth",
            value=(
                "サーバーの成長を3次多項式回帰モデルで予測します。\n"
                "特徴:\n"
                "- 適度なデータポイント数が必要です。\n"
                "- 短期的な予測に適しています。\n"
                "- データの傾向を滑らかに捉えることができます。"
            ),
            inline=False
        )

        embed.add_field(
            name="/prophet_growth",
            value=(
                "サーバーの成長をProphetモデルで予測します。\n"
                "特徴:\n"
                "- 大規模なデータセットに適しています。\n"
                "- 季節性や休日の影響を考慮できます。\n"
                "- 長期的な予測に強いです。"
            ),
            inline=False
        )

        embed.add_field(
            name="/arima_growth",
            value=(
                "サーバーの成長をARIMAモデルで予測します。\n"
                "特徴:\n"
                "- 時系列データに適しています。\n"
                "- データの自己相関を考慮します。\n"
                "- 短期から中期の予測に適しています。"
            ),
            inline=False
        )

        embed.set_footer(text="この予測は統計モデルに基づくものであり、実際の結果を保証するものではありません。")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    cog = GrowthHelp(bot)
    await bot.add_cog(cog)
    bot.tree.add_command(cog.growth_help)