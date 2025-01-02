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

    @discord.app_commands.command(name="growth", description="Predict the server's growth.")
    async def growth(self, interaction: discord.Interaction, target: int):

        guild = interaction.guild
        members = guild.members

        join_dates = [member.joined_at for member in members if member.joined_at is not None]
        join_dates.sort()

        if len(join_dates) < 2:
            await interaction.response.send_message("Insufficient data to perform regression analysis.")
            return

        X = np.array([d.toordinal() for d in join_dates]).reshape(-1, 1)
        y = np.arange(1, len(join_dates) + 1)

        # Use polynomial features for a more detailed model
        poly = PolynomialFeatures(degree=2)
        X_poly = poly.fit_transform(X)
        model = LinearRegression()
        model.fit(X_poly, y)

        coef = model.coef_
        intercept = model.intercept_

        # Predict the ordinal date for the target
        # For the inverse, we solve target = model(X_poly) => target = coef*X_poly + intercept
        # We estimate it with Newton's method or a simple approximate search
        # (because it's a quadratic). We'll do a direct solve with the known formula.
        # model: a + b*x + c*x^2 = target
        a = intercept
        b = coef[1] if len(coef) > 1 else 0
        c = coef[2] if len(coef) > 2 else 0
        # c*x^2 + b*x + (a - target) = 0
        A = c
        B = b
        C = a - target

        if abs(A) < 1e-8:  # fallback to linear if c is near zero
            if abs(B) < 1e-8:
                await interaction.response.send_message("No growth detected.")
                return
            else:
                target_date_ordinal = -C / B
        else:
            discriminant = B**2 - 4*A*C
            if discriminant < 0:
                await interaction.response.send_message("No valid predicted date found.")
                return
            # Use only the positive solution
            sol1 = (-B + math.sqrt(discriminant)) / (2*A)
            sol2 = (-B - math.sqrt(discriminant)) / (2*A)
            target_date_ordinal = sol1 if sol1 > 0 else sol2

        if target_date_ordinal <= 0:
            await interaction.response.send_message("No valid predicted date found.")
            return

        target_date = datetime.fromordinal(int(round(target_date_ordinal)))

        # Plot
        plt.style.use('seaborn-whitegrid')
        plt.figure(figsize=(10, 6))
        plt.scatter(join_dates, y, color='blue', label='Actual Data')
        plt.plot(join_dates, model.predict(X_poly), color='red', label='Regression Curve')
        plt.axhline(y=target, color='green', linestyle='--', label=f'Target: {target}')
        plt.axvline(x=target_date, color='purple', linestyle='--', label=f'Predicted Date: {target_date.date()}')
        plt.xlabel('Date Joined')
        plt.ylabel('Member Count')
        plt.title('Server Growth Prediction')
        plt.legend()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        file = discord.File(buf, filename='growth_prediction.png')
        await interaction.response.send_message(file=file, content=f'Predicted date for reaching {target} members: {target_date.date()}')
async def setup(bot):
    await bot.add_cog(Growth(bot))