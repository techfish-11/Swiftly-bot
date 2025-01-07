import discord
from discord.ext import commands
import numpy as np
from datetime import datetime
import pandas as pd
import io
import matplotlib.pyplot as plt

try:
    from prophet import Prophet
except ImportError:
    from fbprophet import Prophet

class ProphetGrowth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="prophet_growth", description="サーバーの成長を予測します。Prophetは大規模サーバー向けです。")
    async def prophet_growth(self, interaction: discord.Interaction, target: int):
        await interaction.response.defer(thinking=True)
        
        try:
            guild = interaction.guild
            members = guild.members
            join_dates = [m.joined_at for m in members if m.joined_at]
            join_dates.sort()

            if len(join_dates) < 2:
                await interaction.followup.send("予測を行うためのデータが不足しています。")
                return

            data = {'ds': [d.strftime('%Y-%m-%d') for d in join_dates], 'y': np.arange(1, len(join_dates) + 1)}
            df = pd.DataFrame(data)

            # Send initial progress message
            progress_message = await interaction.followup.send("データを処理中... 0%")

            model = Prophet()
            model.fit(df)

            # Update progress
            await progress_message.edit(content="データを処理中... 50%")

            future = model.make_future_dataframe(periods=92)
            forecast = model.predict(future)

            # Update progress
            await progress_message.edit(content="データを処理中... 75%")

            found_date = None
            for i, row in forecast.iterrows():
                if row['yhat'] >= target:
                    found_date = row['ds']
                    break

            if not found_date:
                await progress_message.edit(content="予測範囲内でその目標値に到達しません。")
                return

            plt.figure(figsize=(12, 8))
            plt.scatter(join_dates, np.arange(1, len(join_dates) + 1), color='blue', label='Actual Data', alpha=0.6)
            plt.plot(forecast['ds'], forecast['yhat'], color='red', label='Prediction', linewidth=2)
            plt.axhline(y=target, color='green', linestyle='--', label=f'Target: {target}', linewidth=2)
            plt.axvline(x=found_date, color='purple', linestyle='--', label=f'Predicted: {found_date}', linewidth=2)
            plt.xlabel('Join Date', fontsize=14)
            plt.ylabel('Member Count', fontsize=14)
            plt.title('Server Growth Prediction with Prophet', fontsize=16)
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.7)

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plt.close()

            file = discord.File(buf, filename='prophet_growth_prediction.png')
            embed = discord.Embed(title="Server Growth Prediction with Prophet", description=f'{target}人に達する予測日: {found_date}', color=discord.Color.blue())
            embed.set_image(url="attachment://prophet_growth_prediction.png")
            embed.add_field(name="データポイント数", value=str(len(join_dates)), inline=True)
            embed.add_field(name="最初の参加日", value=join_dates[0].strftime('%Y-%m-%d'), inline=True)
            embed.add_field(name="最新の参加日", value=join_dates[-1].strftime('%Y-%m-%d'), inline=True)
            embed.add_field(name="予測モデル", value="Prophet", inline=True)
            embed.set_footer(text="この予測は統計モデルに基づくものであり、実際の結果を保証するものではありません。\nHosted by TechFish_Lab")

            await progress_message.edit(content="予測完了！", embed=embed)
            await interaction.followup.send(file=file)
        except Exception as e:
            await interaction.followup.send(f"エラーが発生しました: {str(e)}")

async def setup(bot):
    await bot.add_cog(ProphetGrowth(bot))