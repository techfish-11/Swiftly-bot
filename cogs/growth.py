import discord
from discord.ext import commands
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression
import io
from sklearn.preprocessing import PolynomialFeatures

import matplotlib.pyplot as plt

class Growth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="growth", description="サーバーの成長を予測します。")
    async def growth(self, interaction: discord.Interaction, target: int):

        guild = interaction.guild
        members = guild.members
        join_dates = [m.joined_at for m in members if m.joined_at]
        join_dates.sort()

        if len(join_dates) < 2:
            await interaction.response.send_message("回帰分析を行うためのデータが不足しています。")
            return

        X = np.array([d.toordinal() for d in join_dates]).reshape(-1, 1)
        y = np.arange(1, len(join_dates) + 1)

        poly = PolynomialFeatures(degree=2)
        X_poly = poly.fit_transform(X)
        model = LinearRegression()
        model.fit(X_poly, y)

        # 目標メンバー数に達する日を探索
        start_day = X[-1][0]
        found_date = None
        for i in range(36500):
            test_day = start_day + i
            pred = model.predict(poly.transform([[test_day]]))[0]
            if pred >= target:
                found_date = datetime.fromordinal(int(test_day))
                break

        if not found_date:
            await interaction.response.send_message("予測範囲内でその目標値に到達しません。")
            return

        X_plot = np.linspace(X[0][0], test_day, 200).reshape(-1, 1)
        y_plot = model.predict(poly.transform(X_plot))

        plt.figure(figsize=(10, 6))
        plt.scatter(join_dates, y, color='blue', label='Actual Data')
        plt.plot([datetime.fromordinal(int(x[0])) for x in X_plot], y_plot, color='red', label='Prediction')
        plt.axhline(y=target, color='green', linestyle='--', label=f'Target: {target}')
        plt.axvline(x=found_date, color='purple', linestyle='--', label=f'Predicted: {found_date.date()}')
        plt.xlabel('Join Date')
        plt.ylabel('Member Count')
        plt.title('Server Growth Prediction')
        plt.legend()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        file = discord.File(buf, filename='growth_prediction.png')
        await interaction.response.send_message(file=file, content=f'{target}人に達する予測日: {found_date.date()}')

async def setup(bot):
    await bot.add_cog(Growth(bot))