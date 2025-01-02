import discord
from discord.ext import commands
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression
import io

import matplotlib.pyplot as plt

class Growth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="growth", description="サーバーの成長を予測します。")
    async def growth(self, interaction: discord.Interaction, target: int):
        await interaction.response.defer(thinking=True)  # Show "考え中..." to prevent timeout
        guild = interaction.guild
        members = guild.members

        join_dates = [member.joined_at for member in members if member.joined_at is not None]
        join_dates.sort()

        if len(join_dates) < 2:
            await interaction.response.send_message("回帰分析を行うためのデータが不足しています。")
            return

        X = np.array([d.toordinal() for d in join_dates]).reshape(-1, 1)
        y = np.arange(1, len(join_dates) + 1)

        model = LinearRegression()
        model.fit(X, y)

        coef = model.coef_[0]
        intercept = model.intercept_

        if coef == 0:
            await interaction.response.send_message("成長が確認できませんでした。")
            return

        # 目標メンバー数に達する日を計算
        target_date_ordinal = (target - intercept) / coef
        target_date = datetime.fromordinal(int(round(target_date_ordinal)))

        plt.figure(figsize=(10, 6))
        plt.scatter(join_dates, y, color='blue', label='Actual Data')
        plt.plot(join_dates, model.predict(X), color='red', label='Regression Line')
        plt.axhline(y=target, color='green', linestyle='--', label=f'Target: {target}')
        plt.axvline(x=target_date, color='purple', linestyle='--', label=f'Predicted Date: {target_date.date()}')
        plt.xlabel('Join Date')
        plt.ylabel('Member Count')
        plt.title('Server Growth Prediction')
        plt.legend()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        file = discord.File(buf, filename='growth_prediction.png')
        await interaction.response.send_message(file=file, content=f'{target}人に達する予測日: {target_date.date()}')

async def setup(bot):
    await bot.add_cog(Growth(bot))