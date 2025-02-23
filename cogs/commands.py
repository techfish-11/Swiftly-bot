import discord
from discord.ext import commands
import math

class CommandListView(discord.ui.View):
    def __init__(self, commands_list, timeout=180):
        super().__init__(timeout=timeout)
        self.commands_list = commands_list
        self.current_page = 0
        self.items_per_page = 10
        self.max_pages = math.ceil(len(commands_list) / self.items_per_page)

    def get_embed(self):
        start_idx = self.current_page * self.items_per_page
        end_idx = start_idx + self.items_per_page
        current_commands = self.commands_list[start_idx:end_idx]

        embed = discord.Embed(
            title="Swiftlyのコマンド一覧",
            description=f"ページ {self.current_page + 1}/{self.max_pages}",
            color=discord.Color.green()
        )

        for command in current_commands:
            embed.add_field(
                name=f"/{command.name}",
                value=command.description if command.description else "説明なし",
                inline=False
            )

        return embed

    @discord.ui.button(label="前へ", style=discord.ButtonStyle.gray)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            await interaction.response.edit_message(embed=self.get_embed(), view=self)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="次へ", style=discord.ButtonStyle.gray)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.max_pages - 1:
            self.current_page += 1
            await interaction.response.edit_message(embed=self.get_embed(), view=self)
        else:
            await interaction.response.defer()

class CommandList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="help-command", description="Swiftlyが提供するすべてのコマンドを表示します。")
    async def command_list(self, interaction: discord.Interaction):
        """Botが提供するすべてのコマンドとその説明を表示"""
        commands_list = self.bot.tree.get_commands()
        view = CommandListView(list(commands_list))
        await interaction.response.send_message(embed=view.get_embed(), view=view)

async def setup(bot):
    await bot.add_cog(CommandList(bot))
