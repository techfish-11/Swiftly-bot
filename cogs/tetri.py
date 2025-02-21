import asyncio
import random
import copy
import discord
from discord.ext import commands
from discord import app_commands

# 定数設定
BOARD_WIDTH = 10
BOARD_HEIGHT = 15
EMPTY = "⬛"

# 各テトリミノに対応する色（emoji）
COLOR_MAP = {
    0: "🟦",  # I
    1: "🟨",  # O
    2: "🟪",  # T
    3: "🟩",  # S
    4: "🟥",  # Z
    5: "🟧",  # J
    6: "🟫"   # L
}

# テトリミノの定義（各座標は原点からの相対座標）
TETRIS_SHAPES = [
    [(0, 0), (0, 1), (0, 2), (0, 3)],          # I
    [(0, 0), (1, 0), (0, 1), (1, 1)],          # O
    [(0, 0), (-1, 1), (0, 1), (1, 1)],         # T
    [(0, 0), (1, 0), (0, 1), (-1, 1)],         # S
    [(0, 0), (-1, 0), (0, 1), (1, 1)],         # Z
    [(0, 0), (0, 1), (0, 2), (-1, 2)],         # J
    [(0, 0), (0, 1), (0, 2), (1, 2)]           # L
]

class TetrisGame:
    def __init__(self):
        # 0: empty, >0: fixed block (type index + 1)
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_piece = None  # {x, y, shape, type}
        self.game_over = False
        self.spawn_piece()

    def spawn_piece(self):
        spawn_x = BOARD_WIDTH // 2
        spawn_y = 0
        type_index = random.randint(0, len(TETRIS_SHAPES) - 1)
        shape = copy.deepcopy(TETRIS_SHAPES[type_index])
        piece = {"x": spawn_x, "y": spawn_y, "shape": shape, "type": type_index}
        # 当たり判定チェック
        if any(not self.is_cell_empty(spawn_x + dx, spawn_y + dy) for (dx, dy) in piece["shape"]):
            self.game_over = True
        else:
            self.current_piece = piece

    def is_cell_empty(self, x: int, y: int) -> bool:
        if not (0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT):
            return False
        return self.board[y][x] == 0

    def current_piece_positions(self):
        if self.current_piece is None:
            return []
        x = self.current_piece["x"]
        y = self.current_piece["y"]
        return [(x + dx, y + dy) for (dx, dy) in self.current_piece["shape"]]

    def fix_piece(self):
        if self.current_piece is None:
            return
        # 固定ブロックはテトリミノの種類に応じた値（type_index+1）を保存
        for (x, y) in self.current_piece_positions():
            if 0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT:
                self.board[y][x] = self.current_piece["type"] + 1
        self.current_piece = None
        self.remove_complete_lines()
        self.spawn_piece()

    def remove_complete_lines(self):
        new_board = [row for row in self.board if not all(cell != 0 for cell in row)]
        lines_cleared = BOARD_HEIGHT - len(new_board)
        for _ in range(lines_cleared):
            new_board.insert(0, [0 for _ in range(BOARD_WIDTH)])
        self.board = new_board

    def can_move(self, dx: int, dy: int, new_shape=None) -> bool:
        if self.current_piece is None:
            return False
        shape = new_shape if new_shape is not None else self.current_piece["shape"]
        new_x = self.current_piece["x"] + dx
        new_y = self.current_piece["y"] + dy
        for (offset_x, offset_y) in shape:
            x = new_x + offset_x
            y = new_y + offset_y
            if not (0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT):
                return False
            if self.board[y][x] != 0:
                return False
        return True

    def move_left(self):
        if self.current_piece and self.can_move(-1, 0):
            self.current_piece["x"] -= 1

    def move_right(self):
        if self.current_piece and self.can_move(1, 0):
            self.current_piece["x"] += 1

    def move_down(self) -> bool:
        if self.current_piece and self.can_move(0, 1):
            self.current_piece["y"] += 1
            return True
        else:
            self.fix_piece()
            return False

    def drop(self):
        while self.current_piece and self.can_move(0, 1):
            self.current_piece["y"] += 1
        self.fix_piece()

    def rotate(self):
        if self.current_piece is None:
            return
        old_shape = self.current_piece["shape"]
        rotated_shape = [(-dy, dx) for (dx, dy) in old_shape]
        old_cx = sum(x for x, _ in old_shape) / len(old_shape)
        old_cy = sum(y for _, y in old_shape) / len(old_shape)
        new_cx = sum(x for x, _ in rotated_shape) / len(rotated_shape)
        new_cy = sum(y for _, y in rotated_shape) / len(rotated_shape)
        offset_x = round(old_cx - new_cx)
        offset_y = round(old_cy - new_cy)
        adjusted_shape = [(x + offset_x, y + offset_y) for (x, y) in rotated_shape]
        if self.can_move(0, 0, new_shape=adjusted_shape):
            self.current_piece["shape"] = adjusted_shape

    def render(self) -> str:
        display = [[EMPTY for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        # 固定ブロックの描画（boardの値 > 0 のとき対応する色を表示）
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board[y][x] != 0:
                    color_index = self.board[y][x] - 1
                    display[y][x] = COLOR_MAP[color_index]
        # 落下中のブロックの描画
        if self.current_piece:
            piece_color = COLOR_MAP[self.current_piece["type"]]
            for (x, y) in self.current_piece_positions():
                if 0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT:
                    display[y][x] = piece_color
        return "\n".join("".join(row) for row in display)

class TetrisView(discord.ui.View):
    def __init__(self, game: TetrisGame, interaction: discord.Interaction):
        super().__init__(timeout=120)
        self.game = game
        self.interaction = interaction

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.interaction.user.id:
            await interaction.response.send_message("このゲームはあなたの操作ではありません。", ephemeral=True)
            return False
        return True

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
        self.game.move_down()
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
        self.game.rotate()
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
        view = TetrisView(game, interaction)
        await interaction.response.send_message(embed=embed, view=view)
        
        async def auto_drop(view: TetrisView):
            await asyncio.sleep(3)
            while not game.game_over:
                await asyncio.sleep(3)
                if game.current_piece and game.can_move(0, 1):
                    game.move_down()
                await view.update_message()
        
        self.bot.loop.create_task(auto_drop(view))

async def setup(bot):
    await bot.add_cog(Tetri(bot))
