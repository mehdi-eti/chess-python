import os
import pygame

from src.sound import Sound
from src.theme import Theme
from src.const import GREEN_THEME, GRAY_THEME


class Config:
    def __init__(self):
        self.themes: list[Theme] = []
        self._add_themes()
        self.idx = 0
        self.theme: Theme = self.themes[self.idx]
        self.font = pygame.font.SysFont('monospace', 18, bold=True)
        self.move_sound = Sound(os.path.join('assets/sounds/move.wav'))
        self.capture_sound = Sound(os.path.join('assets/sounds/capture.wav'))

    def change_theme(self):
        self.idx += 1
        # for reset theme index
        self.idx %= len(self.themes)  # [t1, t2, t3, t4]
        self.theme = self.themes[self.idx]

    def _add_themes(self):
        green = Theme(**GREEN_THEME)
        gray = Theme(**GRAY_THEME)

        self.themes = [green, gray]
