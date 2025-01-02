import discord
from discord.ext import commands
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression
import io
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import KFold, cross_val_score
from statsmodels.tsa.arima.model import ARIMA

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

        # Linear Regression Model
        model = LinearRegression()
        model.fit(X, y)
        future_days = np.arange(X[-1][0], X[-1][0] + 36500).reshape(-1, 1)
        predictions = model.predict(future_days)

        found_date = None
        for i, pred in enumerate(predictions):
            if pred >= target:
                found_date = datetime.fromordinal(int(future_days[i][0]))
                break

        if not found_date:
            await interaction.response.send_message("予測範囲内でその目標値に到達しません。")
            return

        X_plot = np.linspace(X[0][0], found_date.toordinal(), 200).reshape(-1, 1)
        y_plot = model.predict(X_plot)

        plt.figure(figsize=(12, 8))
        plt.scatter(join_dates, y, color='blue', label='Actual Data', alpha=0.6)
        plt.plot([datetime.fromordinal(int(x[0])) for x in X_plot], y_plot, color='red', label='Prediction', linewidth=2)
        plt.axhline(y=target, color='green', linestyle='--', label=f'Target: {target}', linewidth=2)
        plt.axvline(x=found_date, color='purple', linestyle='--', label=f'Predicted: {found_date.date()}', linewidth=2)
        plt.xlabel('Join Date', fontsize=14)
        plt.ylabel('Member Count', fontsize=14)
        plt.title('Server Growth Prediction', fontsize=16)
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        file = discord.File(buf, filename='growth_prediction.png')
        embed = discord.Embed(title="Server Growth Prediction", description=f'{target}人に達する予測日: {found_date.date()}', color=discord.Color.blue())
        embed.set_image(url="attachment://growth_prediction.png")
        embed.add_field(name="データポイント数", value=str(len(join_dates)), inline=True)
        embed.add_field(name="予測精度", value=f"{model.score(X, y):.2f}", inline=True)
        embed.set_footer(text="この予測は統計モデルに基づくものであり、実際の結果を保証するものではありません。")
        

        await interaction.response.send_message(embed=embed, file=file)

async def setup(bot):
    await bot.add_cog(Growth(bot))