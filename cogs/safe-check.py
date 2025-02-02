import discord
from discord.ext import commands
import re

class SafeCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.discord_invite_pattern = re.compile(r'discord\.gg/\w+|discord\.com/invite/\w+')
        self.admin_user_ids = [1241397634095120438, 1132696836054995146]

    async def is_admin(self, user_id: int) -> bool:
        return user_id == self.admin_user_id

    @discord.app_commands.command(name='blacklist-add', description='Add a server ID to blacklist')
    async def blacklist_add(self, interaction: discord.Interaction, server_id: str):
        if not await self.is_admin(interaction.user.id):
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=False)
            return

        try:
            with open('blacklist.txt', 'r') as f:
                blacklist = [line.strip() for line in f.readlines()]
            
            if server_id in blacklist:
                await interaction.response.send_message("This server ID is already in the blacklist.", ephemeral=False)
                return

            with open('blacklist.txt', 'a') as f:
                f.write(f"{server_id}\n")
            
            await interaction.response.send_message(f"Server ID {server_id} has been added to the blacklist.", ephemeral=False)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=False)

    @discord.app_commands.command(name='blacklist-remove', description='Remove a server ID from blacklist')
    async def blacklist_remove(self, interaction: discord.Interaction, server_id: str):
        if not await self.is_admin(interaction.user.id):
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=False)
            return

        try:
            with open('blacklist.txt', 'r') as f:
                blacklist = [line.strip() for line in f.readlines()]
            
            if server_id not in blacklist:
                await interaction.response.send_message("This server ID is not in the blacklist.", ephemeral=False)
                return

            blacklist.remove(server_id)
            
            with open('blacklist.txt', 'w') as f:
                f.write('\n'.join(blacklist) + '\n' if blacklist else '')
            
            await interaction.response.send_message(f"Server ID {server_id} has been removed from the blacklist.", ephemeral=False)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=False)

    @discord.app_commands.command(name='blacklist-search', description='Search for a server ID in blacklist')
    async def blacklist_search(self, interaction: discord.Interaction, server_id: str):
        if not await self.is_admin(interaction.user.id):
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=False)
            return

        try:
            with open('blacklist.txt', 'r') as f:
                blacklist = [line.strip() for line in f.readlines()]
            
            is_blacklisted = server_id in blacklist
            await interaction.response.send_message(
                f"Server ID {server_id} is{' ' if is_blacklisted else ' not '}in the blacklist.",
                ephemeral=False
            )
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=False)

    @discord.app_commands.command(name='blacklist-list', description='List all blacklisted server IDs')
    async def blacklist_list(self, interaction: discord.Interaction):
        if not await self.is_admin(interaction.user.id):
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=False)
            return

        try:
            with open('blacklist.txt', 'r') as f:
                blacklist = [line.strip() for line in f.readlines()]
            
            if not blacklist:
                await interaction.response.send_message("The blacklist is empty.", ephemeral=False)
                return

            embed = discord.Embed(title="Blacklisted Server IDs", color=discord.Color.red())
            embed.description = '\n'.join(blacklist)
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=False)

async def setup(bot):
    await bot.add_cog(SafeCheck(bot))
