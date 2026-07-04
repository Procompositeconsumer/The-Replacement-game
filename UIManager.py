import os
import pygame

from settings import *
from engine.button import Button


class UIManager:

    def __init__(self):
        button_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
        button_y = SCREEN_HEIGHT - BUTTON_HEIGHT - 40
        self.return_to_menu_button = Button(button_x, button_y, "Return to Menu?")
        self.return_to_menu_button_visible = False
        self.return_to_menu_button_start = None
        self.return_to_menu_button_delay = 1000
        self.vine_boom_sound = self._load_sound("VineBoom.ogg")
        self.return_button_boom_played = False

    def _load_sound(self, filename):
        path = os.path.join(os.path.dirname(__file__), filename)
        if not os.path.isfile(path):
            return None
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            return pygame.mixer.Sound(path)
        except Exception:
            return None

    def _play_vine_boom(self):
        if self.vine_boom_sound is None:
            return
        try:
            self.vine_boom_sound.play()
        except Exception:
            pass

    def hide_return_button(self):
        self.return_to_menu_button_visible = False
        self.return_to_menu_button_start = None
        self.return_button_boom_played = False

    def show_return_button(self):
        if not self.return_to_menu_button_visible and self.return_to_menu_button_start is None:
            self.return_to_menu_button_start = pygame.time.get_ticks()
            self.return_button_boom_played = False

    def update(self):
        if not self.return_to_menu_button_visible and self.return_to_menu_button_start is not None:
            elapsed = pygame.time.get_ticks() - self.return_to_menu_button_start
            if elapsed >= self.return_to_menu_button_delay:
                self.return_to_menu_button_visible = True
                if not self.return_button_boom_played:
                    self._play_vine_boom()
                    self.return_button_boom_played = True

        if self.return_to_menu_button_visible:
            self.return_to_menu_button.update()

    def draw(self, screen):
        if self.return_to_menu_button_visible:
            self.return_to_menu_button.draw(screen)

    def handle_return_click(self, event):
        if not self.return_to_menu_button_visible:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.return_to_menu_button.clicked(event)

        return False
