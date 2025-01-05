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
        await interaction.response.defer(thinking=True)
        
        guild = interaction.guild
        members = guild.members
        join_dates = [m.joined_at for m in members if m.joined_at]
        join_dates.sort()

        if len(join_dates) < 2:
            await interaction.followup.send("回帰分析を行うためのデータが不足しています。")
            return

        X = np.array([d.toordinal() for d in join_dates]).reshape(-1, 1)
        y = np.arange(1, len(join_dates) + 1)

        # ARIMA Model
        model = ARIMA(y, order=(5, 1, 0))
        model_fit = model.fit(disp=0)
        future_steps = 365
        forecast = model_fit.forecast(steps=future_steps)[0]

        found_date = None
        for i, pred in enumerate(forecast):
            if pred >= target:
                found_date = datetime.fromordinal(int(X[-1][0] + i))
                break

        if not found_date:
            await interaction.followup.send("予測範囲内でその目標値に到達しません。")
            return

        plt.figure(figsize=(12, 8))
        plt.plot(join_dates, y, color='blue', label='Actual Data', alpha=0.6)
        plt.plot([datetime.fromordinal(int(X[-1][0] + i)) for i in range(future_steps)], forecast, color='red', label='Prediction', linewidth=2)
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
        embed.add_field(name="予測精度 (AIC)", value=f"{model_fit.aic:.2f}", inline=True)
        embed.add_field(name="最初の参加日", value=join_dates[0].strftime('%Y-%m-%d'), inline=True)
        embed.add_field(name="最新の参加日", value=join_dates[-1].strftime('%Y-%m-%d'), inline=True)
        embed.add_field(name="予測モデル", value="ARIMA", inline=True)
        embed.add_field(name="予測範囲", value=f"{future_steps}日", inline=True)
        embed.add_field(name="目標値", value=str(target), inline=True)
        embed.add_field(name="予測された日付", value=found_date.strftime('%Y-%m-%d'), inline=True)
        embed.set_footer(text="この予測は統計モデルに基づくものであり、実際の結果を保証するものではありません。")

        await interaction.followup.send(embed=embed, file=file)

async def setup(bot):
    await bot.add_cog(Growth(bot))