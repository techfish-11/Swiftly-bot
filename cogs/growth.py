import discord
from discord.ext import commands
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression
import io
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import KFold, cross_val_score
from statsmodels.tsa.arima.model import ARIMA
import asyncio

import matplotlib.pyplot as plt

class Growth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="growth", description="サーバーの成長を予測します。全サーバー向きです。")
    async def growth(self, interaction: discord.Interaction, target: int, show_graph: bool = True):
        try:
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

            # Polynomial Regression Model (3rd degree)
            poly = PolynomialFeatures(degree=3)
            X_poly = poly.fit_transform(X)
            model = LinearRegression()
            model.fit(X_poly, y)
            future_days = np.arange(X[-1][0], X[-1][0] + 36500).reshape(-1, 1)
            future_days_poly = poly.transform(future_days)
            
            # Progress bar simulation
            for i in range(0, 101, 10):
                await interaction.followup.send(f"計算中... {i}%", ephemeral=True)
                await asyncio.sleep(0.1)  # Simulate progress

            predictions = model.predict(future_days_poly)

            found_date = None
            for i, pred in enumerate(predictions):
                if pred >= target:
                    found_date = datetime.fromordinal(int(future_days[i][0]))
                    break

            if not found_date:
                await interaction.followup.send("予測範囲内でその目標値に到達しません。")
                return

            if show_graph:
                X_plot = np.linspace(X[0][0], found_date.toordinal(), 200).reshape(-1, 1)
                X_plot_poly = poly.transform(X_plot)
                y_plot = model.predict(X_plot_poly)

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
            else:
                embed = discord.Embed(title="Server Growth Prediction", description=f'{target}人に達する予測日: {found_date.date()}', color=discord.Color.blue())

            embed.add_field(name="データポイント数", value=str(len(join_dates)), inline=True)
            embed.add_field(name="予測精度", value=f"{model.score(X_poly, y):.2f}", inline=True)
            embed.add_field(name="最初の参加日", value=join_dates[0].strftime('%Y-%m-%d'), inline=True)
            embed.add_field(name="最新の参加日", value=join_dates[-1].strftime('%Y-%m-%d'), inline=True)
            embed.add_field(name="予測モデル", value="3次多項式回帰", inline=True)
            embed.set_footer(text="この予測は統計モデルに基づくものであり、実際の結果を保証するものではありません。")

            if show_graph:
                await interaction.followup.send(embed=embed, file=file)
            else:
                await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"エラーが発生しました: {str(e)}")

async def setup(bot):
    await bot.add_cog(Growth(bot))