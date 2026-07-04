import os
import pygame

from settings import *


class CutsceneManager:

    def __init__(self):
        cutscene_image = pygame.image.load(
            os.path.join(os.path.dirname(__file__), "FirstCutscene.PNG")
        ).convert_alpha()
        image_w, image_h = cutscene_image.get_size()
        scale = min(SCREEN_WIDTH / image_w, SCREEN_HEIGHT / image_h)
        target_w = int(image_w * scale)
        target_h = int(image_h * scale)
        self.cutscene_background = pygame.transform.smoothscale(
            cutscene_image,
            (target_w, target_h)
        )
        self.cutscene_rect = self.cutscene_background.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.show_cutscene = False
        self.cutscene_alpha = 0
        self.cutscene_fade_speed = 3

    def update(self):
        if self.show_cutscene and self.cutscene_alpha < 255:
            self.cutscene_alpha += self.cutscene_fade_speed
            if self.cutscene_alpha > 255:
                self.cutscene_alpha = 255

    def draw(self, screen):
        if self.show_cutscene:
            cutscene = self.cutscene_background.copy()
            cutscene.set_alpha(self.cutscene_alpha)
            screen.blit(cutscene, self.cutscene_rect)
