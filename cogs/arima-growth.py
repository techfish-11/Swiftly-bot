import discord
from discord.ext import commands
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression
import io
from statsmodels.tsa.arima.model import ARIMA

import matplotlib.pyplot as plt

class ARIMAGrowth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="arima_growth", description="サーバーの成長をARIMAモデルで予測します。")
    async def arima_growth(self, interaction: discord.Interaction, target: int, show_graph: bool = True):
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

            # Narrow down the search space for ARIMA parameters to reduce resource usage
            possible_orders = [(0, 1, 0), (1, 1, 0), (1, 1, 1), (2, 1, 0)]
            best_order = None
            best_aic = float('inf')
            for order in possible_orders:
                try:
                    temp_model = ARIMA(y, order=order)
                    temp_fit = temp_model.fit()
                    if temp_fit.aic < best_aic:
                        best_aic = temp_fit.aic
                        best_order = order
                except:
                    pass

            model = ARIMA(y, order=best_order)
            model_fit = model.fit()
            predictions = model_fit.forecast(steps=365)

            found_date = None
            for i, pred in enumerate(predictions):
                if pred >= target:
                    found_date = datetime.fromordinal(int(X[-1][0] + i))
                    break

            if not found_date:
                await interaction.followup.send("予測範囲内でその目標値に到達しません。")
                return

            if show_graph:
                plt.figure(figsize=(8, 5))
                plt.scatter(join_dates, y, color='blue', label='Actual Data', alpha=0.6)
                pred_dates = [datetime.fromordinal(int(X[-1][0] + i)) for i in range(len(predictions))]
                plt.plot(pred_dates, predictions, color='red', label='Prediction', linewidth=2)
                plt.axhline(y=target, color='green', linestyle='--', label=f'Target: {target}', linewidth=2)
                plt.axvline(x=found_date, color='purple', linestyle='--', label=f'Predicted: {found_date.date()}', linewidth=2)
                plt.xlabel('Join Date')
                plt.ylabel('Member Count')
                plt.title('Server Growth Prediction (ARIMA)')
                plt.legend()
                plt.grid(True, linestyle='--', alpha=0.7)

                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                plt.close()

                file = discord.File(buf, filename='arima_growth_prediction.png')
                embed = discord.Embed(
                    title="Server Growth Prediction (ARIMA)",
                    description=f'{target}人に達する予測日: {found_date.date()}',
                    color=discord.Color.blue()
                )
                embed.set_image(url="attachment://arima_growth_prediction.png")
            else:
                embed = discord.Embed(
                    title="Server Growth Prediction (ARIMA)",
                    description=f'{target}人に達する予測日: {found_date.date()}',
                    color=discord.Color.blue()
                )

            embed.add_field(name="データポイント数", value=str(len(join_dates)), inline=True)
            embed.add_field(name="最適パラメータ", value=str(best_order), inline=True)
            embed.add_field(name="AIC", value=f"{model_fit.aic:.2f}", inline=True)
            embed.add_field(name="最初の参加日", value=join_dates[0].strftime('%Y-%m-%d'), inline=True)
            embed.add_field(name="最新の参加日", value=join_dates[-1].strftime('%Y-%m-%d'), inline=True)
            embed.add_field(name="予測モデル", value="ARIMA", inline=True)
            embed.set_footer(text="この予測は統計モデルに基づくものであり、実際の結果を保証するものではありません。この機能はベータバージョンです。")

            if show_graph:
                await interaction.followup.send(embed=embed, file=file)
            else:
                await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f"エラーが発生しました: {e}")

async def setup(bot):
    await bot.add_cog(ARIMAGrowth(bot))