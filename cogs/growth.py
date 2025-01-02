import discord
from discord.ext import commands
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression
import io
import math
from sklearn.preprocessing import PolynomialFeatures

import matplotlib.pyplot as plt

class Growth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="growth", description="サーバーの成長を予測します。")
    async def growth(self, interaction: discord.Interaction, target: int):
        
        await interaction.response.defer(thinking=True)
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

        # Quadratic coefficients a*x^2 + b*x + c
        a = model.coef_[2]
        b = model.coef_[1]
        c = model.intercept_ + model.coef_[0] - target

        disc = b**2 - 4*a*c
        if a == 0 or disc < 0:
            await interaction.response.send_message("成長予測ができませんでした。")
            return
        
        sol1 = (-b + math.sqrt(disc)) / (2*a)
        sol2 = (-b - math.sqrt(disc)) / (2*a)
        future_ordinal = max(sol1, sol2)
        target_date = datetime.fromordinal(int(round(future_ordinal)))

        plt.figure(figsize=(10, 6))
        plt.scatter(join_dates, y, color='blue', label='Actual Data')
        plt.plot(join_dates, model.predict(X_poly), color='red', label='Regression')
        plt.axhline(y=target, color='green', linestyle='--', label=f'Target: {target}')
        plt.axvline(x=target_date, color='purple', linestyle='--', label=f'Predicted: {target_date.date()}')
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