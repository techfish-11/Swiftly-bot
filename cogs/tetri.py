import asyncio
import discord
from discord.ext import commands
from discord import app_commands

# 定数設定
BOARD_WIDTH = 10
BOARD_HEIGHT = 15
# 絵文字での描画
EMPTY = "⬛"
FIXED = "🟦"
FALLING = "🟪"


class TetrisGame:
    def __init__(self):
        # 0: empty, 1: fixed block
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_piece = None  # (x, y)
        self.game_over = False
        self.spawn_piece()

    def spawn_piece(self):
        # 新しいブロックをトップ中央に出現させる
        spawn_x = BOARD_WIDTH // 2
        spawn_y = 0
        if self.board[spawn_y][spawn_x] != 0:
            self.game_over = True
        else:
            self.current_piece = (spawn_x, spawn_y)

    def fix_piece(self):
        if self.current_piece is None:
            return
        x, y = self.current_piece
        self.board[y][x] = 1
        self.current_piece = None
        self.remove_complete_lines()
        self.spawn_piece()

    def remove_complete_lines(self):
        new_board = [row for row in self.board if not all(cell == 1 for cell in row)]
        lines_cleared = BOARD_HEIGHT - len(new_board)
        for _ in range(lines_cleared):
            new_board.insert(0, [0 for _ in range(BOARD_WIDTH)])
        self.board = new_board

    def can_move(self, dx: int, dy: int) -> bool:
        if self.current_piece is None:
            return False
        x, y = self.current_piece
        new_x, new_y = x + dx, y + dy
        if not (0 <= new_x < BOARD_WIDTH and 0 <= new_y < BOARD_HEIGHT):
            return False
        if self.board[new_y][new_x] != 0:
            return False
        return True

    def move_left(self):
        if self.current_piece and self.can_move(-1, 0):
            x, y = self.current_piece
            self.current_piece = (x - 1, y)

    def move_right(self):
        if self.current_piece and self.can_move(1, 0):
            x, y = self.current_piece
            self.current_piece = (x + 1, y)

    def move_down(self) -> bool:
        if self.current_piece and self.can_move(0, 1):
            x, y = self.current_piece
            self.current_piece = (x, y + 1)
            return True
        else:
            self.fix_piece()
            return False

    def drop(self):
        while self.current_piece and self.can_move(0, 1):
            x, y = self.current_piece
            self.current_piece = (x, y + 1)
        self.fix_piece()

    def rotate(self):
        # シングルセルの場合、rotateは動作しない
        pass

    def render(self) -> str:
        render_lines = []
        for y in range(BOARD_HEIGHT):
            line = ""
            for x in range(BOARD_WIDTH):
                if self.current_piece == (x, y):
                    line += FALLING
                elif self.board[y][x] == 1:
                    line += FIXED
                else:
                    line += EMPTY
            render_lines.append(line)
        return "\n".join(render_lines)


class TetrisView(discord.ui.View):
    def __init__(self, game: TetrisGame, interaction: discord.Interaction):
        super().__init__(timeout=120)
        self.game = game
        self.interaction = interaction

    async def update_message(self):
        embed = discord.Embed(
            title="Tetris",
            description=self.game.render(),
            color=discord.Color.blue()
        )
        content = None
        if self.game.game_over:
            content = "Game Over!"
            for child in self.children:
                child.disabled = True
        await self.interaction.edit_original_response(embed=embed, content=content, view=self)

    @discord.ui.button(label="←", style=discord.ButtonStyle.primary)
    async def left(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if self.game.game_over:
            return
        self.game.move_left()
        await self.update_message()

    @discord.ui.button(label="→", style=discord.ButtonStyle.primary)
    async def right(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if self.game.game_over:
            return
        self.game.move_right()
        await self.update_message()

    @discord.ui.button(label="↓", style=discord.ButtonStyle.primary)
    async def down(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if self.game.game_over:
            return
        self.game.move_down()  # move_down will fix piece if it can’t move further
        await self.update_message()

    @discord.ui.button(label="⏬", style=discord.ButtonStyle.primary)
    async def drop(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if self.game.game_over:
            return
        self.game.drop()
        await self.update_message()

    @discord.ui.button(label="↻", style=discord.ButtonStyle.secondary)
    async def rotate_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if self.game.game_over:
            return
        self.game.rotate()  # No-op for single-cell piece
        await self.update_message()


class Tetri(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="tetri", description="Discord上でテトリスを遊びます")
    async def tetri(self, interaction: discord.Interaction) -> None:
        game = TetrisGame()
        embed = discord.Embed(
            title="Tetris",
            description=game.render(),
            color=discord.Color.blue()
        )
        # Send the initial response with the view
        await interaction.response.send_message(embed=embed, view=TetrisView(game, interaction))
        # Retrieve the message just sent to pass to the auto-drop task
        msg = await interaction.original_response()

        async def auto_drop(view: TetrisView):
            await asyncio.sleep(3)
            while not game.game_over:
                await asyncio.sleep(3)
                if game.current_piece and game.can_move(0, 1):
                    game.move_down()
                else:
                    # In move_down(), the piece is fixed automatically if it can't move
                    pass
                try:
                    await view.update_message()
                except Exception:
                    break

        # Start the auto-drop task passing in the view instance
        view = msg.components[0].view
        self.bot.loop.create_task(auto_drop(view))


async def setup(bot):
    await bot.add_cog(Tetri(bot))
