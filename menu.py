import pygame
import random
import sys

from settings import *

from engine.button import Button


class MenuScene:

    def __init__(self, manager):

        self.manager = manager

        

        self.background = pygame.image.load(
            BACKGROUND_FOLDER + "menu.png"
        ).convert()

        self.title_font = pygame.font.SysFont(
            DEFAULT_FONT,
            TITLE_FONT_SIZE,
            bold=True
        )

        

        center_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2

        y = BUTTON_START_Y

        self.new_game = Button(
            center_x,
            y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "New Game"
        )

        y += BUTTON_HEIGHT + BUTTON_SPACING

        self.settings_default_text = "Settings"
        self.settings_custom_text_options = [
            "Not yet...",
            "What do you expect?",
            "COME ON IT IS A 5 DAYS PROJECT!"
        ]
        self.settings_last_custom = None
        self.settings_revert_time = 15000
        self.settings_text_changed_time = None

        self.settings = Button(
            center_x,
            y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            self.settings_default_text
        )

        y += BUTTON_HEIGHT + BUTTON_SPACING

        self.quit = Button(
            center_x,
            y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Quit"
        )

    

    def handle_event(self, event):

        if self.new_game.clicked(event):

            print("Start Game")

            # Coming in Part 2
            # self.manager.change_scene("GAMEPLAY")

        if self.settings.clicked(event):

            print("Settings")
            options = [opt for opt in self.settings_custom_text_options if opt != self.settings_last_custom]
            if not options:
                options = self.settings_custom_text_options.copy()
            self.settings.text = random.choice(options)
            self.settings_last_custom = self.settings.text
            self.settings_text_changed_time = pygame.time.get_ticks()

        if self.quit.clicked(event):

            pygame.quit()

            sys.exit()

    # =====================================

    def update(self):

        self.new_game.update()

        self.settings.update()

        self.quit.update()

        if self.settings_text_changed_time is not None:
            if pygame.time.get_ticks() - self.settings_text_changed_time >= self.settings_revert_time:
                self.settings.text = self.settings_default_text
                self.settings_text_changed_time = None

    # =====================================

    def draw(self, screen):

        screen.blit(self.background, (0, 0))

        title = self.title_font.render(
            GAME_TITLE,
            True,
            WHITE
        )

        title_rect = title.get_rect(
            center=(SCREEN_WIDTH // 2, TITLE_Y)
        )

        screen.blit(title, title_rect)

        self.new_game.draw(screen)

        self.settings.draw(screen)

        self.quit.draw(screen)

        version_font = pygame.font.SysFont(
            DEFAULT_FONT,
            SMALL_FONT_SIZE
        )

        version = version_font.render(
            VERSION,
            True,
            WHITE
        )

        screen.blit(
            version,
            (20, SCREEN_HEIGHT - 35)
        )