# Swiftly DiscordBot.
# Developed by: TechFish_1
import discord
from discord.ext import commands
import asyncio
import os
import dotenv

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# tokenを.envファイルから取得
dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

    # cogsフォルダからCogをロード
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            extension_name = filename[:-3]
            try:
                await bot.load_extension(f'cogs.{extension_name}')
                print(f'Loaded: cogs.{extension_name}')
            except Exception as e:
                print(f'Failed to load: cogs.{extension_name} - {e}')

    # アプリコマンドを同期（slashコマンド等）
    await bot.tree.sync()

if __name__ == '__main__':
    asyncio.run(bot.start(TOKEN))