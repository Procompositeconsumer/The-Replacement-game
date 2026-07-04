import os
import pygame

from settings import *


class EndingManager:

    def __init__(self, black_background):
        self.black_background = black_background

        self.bad_ending_background = self._load_image("BadEnding.png", scale=(SCREEN_WIDTH, SCREEN_HEIGHT), alpha=False)
        if self.bad_ending_background is None:
            self.bad_ending_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.bad_ending_background.fill(WHITE)

        self.bad_ending_game_over_image = self._load_image("GameOver.png", alpha=True)
        self.bad_ending_game_over_size = (371, 200)
        self.bad_ending_game_over_scaled = None

        self.state = None
        self.black_alpha = 0
        self.black_hold_time = 800
        self.black_hold_start = None
        self.overlay_alpha = 0
        self.overlay_fade_speed = 220
        self.text_visible = False
        self.text_delay = 1000
        self.text_start = None
        self.background_visible = False
        self.finished = False
        self.return_to_menu_alpha = 0
        self.return_to_menu_scene_manager = None

        self.vine_boom_sound = self._load_sound("VineBoom.ogg")
        self.bad_ending_boom_played = False
        self.game_over_boom_played = False

    def _load_image(self, filename, scale=None, alpha=False):
        path = os.path.join(os.path.dirname(__file__), filename)
        if not os.path.isfile(path):
            return None
        image = pygame.image.load(path)
        if alpha:
            image = image.convert_alpha()
        else:
            image = image.convert()
        if scale is not None:
            image = pygame.transform.smoothscale(image, scale)
        return image

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

    def start_bad_ending(self, ui_manager=None):
        self.state = "blackening"
        self.black_alpha = 0
        self.black_hold_start = None
        self.overlay_alpha = 0
        self.text_visible = False
        self.text_start = None
        self.background_visible = False
        self.finished = False
        self.return_to_menu_alpha = 0
        self.return_to_menu_scene_manager = None
        self.bad_ending_boom_played = False
        self.game_over_boom_played = False
        if ui_manager is not None:
            ui_manager.hide_return_button()

    def begin_return_to_menu(self, scene_manager=None):
        if self.state is None:
            return
        self.state = "returning_to_menu"
        self.return_to_menu_alpha = 0
        self.return_to_menu_scene_manager = scene_manager

    def update(self, ui_manager=None):
        if self.state is None:
            return

        now = pygame.time.get_ticks()

        if self.state == "blackening":
            self.black_alpha = min(255, self.black_alpha + 2)
            if self.black_alpha >= 255:
                self.state = "hold_black"
                self.black_hold_start = now

        elif self.state == "hold_black":
            if now - self.black_hold_start >= self.black_hold_time:
                self.state = "show_bad_ending"
                self.overlay_alpha = 0
                self.background_visible = True
                self.text_start = now
                if not self.bad_ending_boom_played:
                    self._play_vine_boom()
                    self.bad_ending_boom_played = True

        elif self.state == "show_bad_ending":
            if self.overlay_alpha < 255:
                self.overlay_alpha = min(255, self.overlay_alpha + self.overlay_fade_speed)
            elif not self.text_visible:
                if now - self.text_start >= self.text_delay:
                    self.text_visible = True
                    self.finished = True
                    if not self.game_over_boom_played:
                        self._play_vine_boom()
                        self.game_over_boom_played = True
                    if ui_manager is not None:
                        ui_manager.show_return_button()

        elif self.state == "returning_to_menu":
            self.return_to_menu_alpha = min(255, self.return_to_menu_alpha + self.overlay_fade_speed)
            if self.return_to_menu_alpha >= 255:
                self.state = None
                if self.return_to_menu_scene_manager is not None:
                    self.return_to_menu_scene_manager.change_scene("MENU")

    def draw(self, screen):
        if self.state is None:
            return

        if self.black_alpha > 0:
            black_overlay = self.black_background.copy()
            black_overlay.set_alpha(self.black_alpha)
            screen.blit(black_overlay, (0, 0))

        if self.background_visible:
            bad_overlay = self.bad_ending_background.copy()
            bad_overlay.set_alpha(self.overlay_alpha)
            screen.blit(bad_overlay, (0, 0))

        if self.state == "returning_to_menu":
            black_overlay = self.black_background.copy()
            black_overlay.set_alpha(self.return_to_menu_alpha)
            screen.blit(black_overlay, (0, 0))
            return

        if self.text_visible:
            if self.bad_ending_game_over_image is not None:
                if self.bad_ending_game_over_scaled is None:
                    self.bad_ending_game_over_scaled = pygame.transform.smoothscale(
                        self.bad_ending_game_over_image,
                        self.bad_ending_game_over_size,
                    )
                go_rect = self.bad_ending_game_over_scaled.get_rect(midtop=(SCREEN_WIDTH // 2, 20))
                screen.blit(self.bad_ending_game_over_scaled, go_rect)
            else:
                font = pygame.font.SysFont("Barber Fill", 96, bold=True)
                game_over = font.render("Game Over", True, WHITE)
                go_rect = game_over.get_rect(midtop=(SCREEN_WIDTH // 2, 20))
                screen.blit(game_over, go_rect)

    def is_active(self):
        return self.state is not None
