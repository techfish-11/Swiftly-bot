import discord
from discord.ext import commands
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression
import io
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import KFold, cross_val_score
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd

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
            await interaction.followup.send("ARIMAを実行するためのデータが不足しています。")
            return

        earliest = join_dates[0].date()
        latest = join_dates[-1].date()
        date_range = pd.date_range(start=earliest, end=latest, freq='D')

        count = 0
        idx = 0
        daily_counts = {}
        for day in date_range:
            while idx < len(join_dates) and join_dates[idx].date() == day:
                count += 1
                idx += 1
            daily_counts[day] = count

        ts = pd.Series(daily_counts)
        model = ARIMA(ts, order=(1,1,1))
        result = model.fit()

        forecast_days = 36500
        forecast_index = pd.date_range(start=latest + pd.Timedelta(days=1), periods=forecast_days, freq='D')
        forecast_vals = result.forecast(steps=forecast_days)

        found_date = None
        for i, val in enumerate(forecast_vals):
            if val >= target:
                found_date = forecast_index[i]
                break

        if not found_date:
            await interaction.followup.send("予測範囲内でその目標値に到達しません。")
            return

        # Plot
        full_index = ts.index.append(forecast_index)
        full_values = ts.append(forecast_vals)
        plt.figure(figsize=(12,8))
        plt.plot(ts.index, ts.values, label='Actual', color='blue')
        plt.plot(full_index, full_values, label='Forecast', color='red')
        plt.axhline(y=target, color='green', linestyle='--', label=f'Target: {target}', linewidth=2)
        plt.axvline(x=found_date, color='purple', linestyle='--', label=f'Predicted: {found_date.date()}', linewidth=2)
        plt.xlabel('Date')
        plt.ylabel('Member Count')
        plt.title('Server Growth Prediction (ARIMA)')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        file = discord.File(buf, filename='growth_prediction.png')
        embed = discord.Embed(
            title="Server Growth Prediction",
            description=f'{target}人に達する予測日: {found_date.date()}',
            color=discord.Color.blue()
        )
        embed.set_image(url="attachment://growth_prediction.png")
        embed.add_field(name="データポイント数", value=str(len(join_dates)), inline=True)
        embed.add_field(name="予測精度(AIC)", value=f"{result.aic:.2f}", inline=True)
        embed.add_field(name="最初の参加日", value=join_dates[0].strftime('%Y-%m-%d'), inline=True)
        embed.add_field(name="最新の参加日", value=join_dates[-1].strftime('%Y-%m-%d'), inline=True)
        embed.add_field(name="予測モデル", value="ARIMA(1,1,1)", inline=True)
        embed.set_footer(text="この予測は統計モデルに基づくものであり、実際の結果を保証するものではありません。")

        await interaction.followup.send(embed=embed, file=file)

async def setup(bot):
    await bot.add_cog(Growth(bot))