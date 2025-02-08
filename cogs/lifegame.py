import discord
from discord.ext import commands
from discord import app_commands
import numpy as np
import cv2
import os

class LifeGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='lifegame', description='Start a Life Game simulation')
    async def lifegame(self, interaction: discord.Interaction):
        await interaction.response.send_message("ライフゲームのシミュレーションを開始します...")

        # Initialize the game board
        board_size = 50
        board = np.random.choice([0, 1], size=(board_size, board_size))

        # Create a video writer using AV1 codec
        video_filename = 'lifegame_simulation.mp4'
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        out = cv2.VideoWriter(video_filename, fourcc, 30.0, (board_size * 10, board_size * 10))

        for _ in range(100):  # Run for 100 generations
            frame = self.create_frame(board)
            out.write(frame)
            board = self.next_generation(board)

        out.release()

        await interaction.followup.send(file=discord.File(video_filename))
        os.remove(video_filename)

    def create_frame(self, board):
        cell_size = 10
        frame = np.zeros((board.shape[0] * cell_size, board.shape[1] * cell_size, 3), dtype=np.uint8)
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                if board[i, j] == 1:
                    cv2.rectangle(frame, (j * cell_size, i * cell_size), ((j + 1) * cell_size, (i + 1) * cell_size), (255, 255, 255), -1)
        return frame

    def next_generation(self, board):
        new_board = np.zeros(board.shape, dtype=int)
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                live_neighbors = np.sum(board[max(0, i-1):min(board.shape[0], i+2), max(0, j-1):min(board.shape[1], j+2)]) - board[i, j]
                if board[i, j] == 1 and live_neighbors in [2, 3]:
                    new_board[i, j] = 1
                elif board[i, j] == 0 and live_neighbors == 3:
                    new_board[i, j] = 1
        return new_board

async def setup(bot):
    await bot.add_cog(LifeGame(bot))
