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

        # 日次データを作成
        start_date, end_date = join_dates[0].date(), join_dates[-1].date()
        date_range = [start_date + (datetime.min - datetime.min) for _ in range((end_date - start_date).days + 1)]
        daily_counts = []
        idx = 0
        for d in range((end_date - start_date).days + 1):
            current_day = start_date + np.timedelta64(d, 'D')
            while idx < len(join_dates) and join_dates[idx].date() <= current_day:
                idx += 1
            daily_counts.append(idx)

        # ARIMAを使用した将来予測
        model = ARIMA(daily_counts, order=(1,1,1))
        results = model.fit()
        forecast_days = 365
        forecast = results.forecast(steps=forecast_days)
        
        # 目標到達日を探索
        found_date_arima = None
        for i, val in enumerate(forecast, 1):
            if val >= target:
                found_date_arima = end_date + np.timedelta64(i, 'D')
                break
        
        # 既存の多項式回帰も実行
        X = np.array([d.toordinal() for d in join_dates]).reshape(-1, 1)
        y = np.arange(1, len(join_dates) + 1)
        poly = PolynomialFeatures(degree=3)
        X_poly = poly.fit_transform(X)
        lin_model = LinearRegression()
        lin_model.fit(X_poly, y)
        future_days = np.arange(X[-1][0], X[-1][0] + 36500).reshape(-1, 1)
        future_days_poly = poly.transform(future_days)
        predictions = lin_model.predict(future_days_poly)
        found_date_poly = None
        for i, pred in enumerate(predictions):
            if pred >= target:
                found_date_poly = datetime.fromordinal(int(future_days[i][0]))
                break

        if not found_date_arima and not found_date_poly:
            await interaction.followup.send("予測範囲内でその目標値に到達しません。")
            return

        # 結果表示
        embed = discord.Embed(title="Server Growth Prediction", color=discord.Color.blue())
        if found_date_arima:
            embed.add_field(name="ARIMA予測到達日", value=str(found_date_arima), inline=True)
        if found_date_poly:
            embed.add_field(name="多項式回帰予測到達日", value=str(found_date_poly.date()), inline=True)
        embed.add_field(name="データポイント数", value=str(len(join_dates)), inline=True)
        embed.add_field(name="ARIMAモデル", value=str(results.aic), inline=True)
        embed.set_footer(text="この予測は統計モデルに基づくものであり、実際の結果を保証するものではありません。")

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Growth(bot))