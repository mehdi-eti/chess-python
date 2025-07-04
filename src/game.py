import pygame

from src.const import *
from src.board import Board
from src.dragger import Dragger
from src.square import Square
from src.config import Config


# ----------------------------------------------------------------

class Game:
    def __init__(self):
        self.next_player = "white"
        self.board = Board()
        self.dragger = Dragger()
        self.hovered_sqr: Square | None = None
        self.config = Config()

    def show_bg(self, surface: pygame.SurfaceType):
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

                # row coordinates
                if col == 0:
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    # label coordinates
                    lbl = self.config.font.render(str(ROWS - row), 1, color)
                    lbl_pos = (5, 5 + row * SQSIZE)
                    # blit coordinates
                    surface.blit(lbl, lbl_pos)

                # col coordinates
                if row == 7:
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    # label coordinates
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    lbl_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    # blit coordinates
                    surface.blit(lbl, lbl_pos)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # pieces?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    # all pieces except dragged pieces
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=SMALL_IMG)
                        img = pygame.image.load(piece.texture)
                        img_center = (col * SQSIZE) + (SQSIZE // 2), (row * SQSIZE) + (SQSIZE // 2)
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        theme = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece

            # loop all valid moves
            for move in piece.moves:
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                color = theme.trace.light if pos.row + pos.col % 2 == 0 else theme.trace.dark
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr is not None:
            color = (180, 180, 180)
            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, width=3)

    def next_turn(self):
        self.next_player = "white" if self.next_player == "black" else "black"

    def set_hover(self, row, col):
        if col <= 7 and row <= 7:
            self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset_game(self):
        self.__init__()
