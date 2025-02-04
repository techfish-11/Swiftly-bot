import discord
from discord.ext import commands


class CommandList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="help-command", description="Swiftlyが提供するすべてのコマンドを表示します。")
    async def command_list(self, interaction: discord.Interaction):
        """Botが提供するすべてのコマンドとその説明を表示"""
        embed = discord.Embed(
            title="Swiftlyのコマンド一覧", description="以下はSwiftlyが提供するコマンドとその説明です。", color=discord.Color.green())

        # コマンド一覧の取得
        for command in self.bot.tree.get_commands():
            # コマンド名と説明を埋め込む
            embed.add_field(
                name=f"/{command.name}", value=command.description if command.description else "説明なし", inline=False)

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(CommandList(bot))
