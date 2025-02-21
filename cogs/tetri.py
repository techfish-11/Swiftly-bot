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
        # 簡易的なライン消去処理
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
            # 下に動けなければ固定する
            self.fix_piece()
            return False

    def drop(self):
        # ブロックを最下段まで落とす
        while self.current_piece and self.can_move(0, 1):
            x, y = self.current_piece
            self.current_piece = (x, y + 1)
        self.fix_piece()

    def rotate(self):
        # シングルセルの場合、rotateは動作しない
        pass

    def render(self) -> str:
        # ボードの文字列表現を生成
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
        super().__init__(timeout=120)  # タイムアウトは必要に応じて調整
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
            # 全てのボタンを無効化する
            for child in self.children:
                child.disabled = True
        await self.interaction.edit_original_response(embed=embed, content=content, view=self)
    
    @discord.ui.button(label="←", style=discord.ButtonStyle.primary)
    async def left(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.game_over:
            return
        self.game.move_left()
        await self.update_message()

    @discord.ui.button(label="→", style=discord.ButtonStyle.primary)
    async def right(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.game_over:
            return
        self.game.move_right()
        await self.update_message()

    @discord.ui.button(label="↓", style=discord.ButtonStyle.primary)
    async def down(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.game_over:
            return
        moved = self.game.move_down()
        # 自動で一定間隔落下させた場合の処理もここに組み込めます
        await self.update_message()

    @discord.ui.button(label="⏬", style=discord.ButtonStyle.primary)
    async def drop(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.game_over:
            return
        self.game.drop()
        await self.update_message()

    @discord.ui.button(label="↻", style=discord.ButtonStyle.secondary)
    async def rotate_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.game_over:
            return
        self.game.rotate()  # シングルセルなので実質ノップ
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
        await interaction.response.send_message(embed=embed, view=TetrisView(game, interaction))
        
        # Optional: 自動落下のコルーチン（ここでは簡易的に実装）
        async def auto_drop():
            await asyncio.sleep(3)
            view: TetrisView = interaction.message.components[0].view  # 設定したviewを取得
            while not game.game_over:
                await asyncio.sleep(3)
                if game.current_piece and game.can_move(0, 1):
                    game.move_down()
                    try:
                        await view.update_message()
                    except Exception:
                        break
                else:
                    # ブロックが固定されたので更新後、新たなブロックが出現する
                    try:
                        await view.update_message()
                    except Exception:
                        break
            # ゲームオーバーの場合、viewは自動でボタンを無効化する
                
        # 自動落下タスクをスタート（viewによる更新と競合する可能性があるため要検証）
        self.bot.loop.create_task(auto_drop())


async def setup(bot):
    await bot.add_cog(Tetri(bot))