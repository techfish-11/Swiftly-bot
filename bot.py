# Swiftly DiscordBot.
# Developed by: TechFish_1
import asyncio
import os
import json

import dotenv
import discord
from discord.ext import commands


intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

client = discord.AutoShardedClient(intents=intents)
bot = commands.Bot(command_prefix="sw!", intents=intents, client=client)

# tokenを.envファイルから取得
dotenv.load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

    # cogsフォルダからCogを非同期でロード
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            extension_name = filename[:-3]
            try:
                await bot.load_extension(f"cogs.{extension_name}")
                print(f"Loaded: cogs.{extension_name}")
            except Exception as e:
                print(f"Failed to load: cogs.{extension_name} - {e}")

    # アプリコマンドを同期（slashコマンド等）
    await bot.tree.sync()

    # 初回のユーザー数を集計して書き込み
    await update_user_count()

    # JSONファイルからユーザー数を読み込み、ステータスを更新
    with open("user_count.json", "r", encoding="utf-8") as fp:
        data = json.load(fp)
        user_count = data.get("total_users", 0)
        await bot.change_presence(activity=discord.Game(name=f"{user_count}人のユーザー数"))


@bot.event
async def on_member_join(member):
    await update_user_count()
    await update_bot_status()


@bot.event
async def on_member_remove(member):
    await update_user_count()
    await update_bot_status()


async def update_user_count():
    # サーバー参加者を集計（重複ユーザーは1度のみカウント）
    unique_users = set()
    for guild in bot.guilds:
        for member in guild.members:
            unique_users.add(member.id)
    user_count = len(unique_users)
    print(f"Unique user count: {user_count}")

    # JSONファイルに書き込み
    with open("user_count.json", "w", encoding="utf-8") as fp:
        json.dump({"total_users": user_count}, fp, ensure_ascii=False, indent=4)


async def update_bot_status():
    # JSONファイルからユーザー数を読み込み、ステータスを更新
    with open("user_count.json", "r", encoding="utf-8") as fp:
        data = json.load(fp)
        user_count = data.get("total_users", 0)
        await bot.change_presence(activity=discord.Game(name=f"{user_count}人のユーザー数"))


@bot.event
async def on_command_error(ctx, error):
    print(f"Error: {error}")
    await ctx.send("エラーが発生しました")


if __name__ == "__main__":
    asyncio.run(bot.start(TOKEN))
