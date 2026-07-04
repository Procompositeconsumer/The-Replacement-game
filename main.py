import os
import sys
import asyncio
import pygame

# Ensure the project root is on sys.path so `engine.*` imports work
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from settings import *
from engine.scene_manager import SceneManager


class Game:

    def __init__(self):

        pygame.init()

        pygame.display.set_caption(GAME_TITLE)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()

        self.running = True

        # Scene Manager controls every screen
        self.scene_manager = SceneManager(self.screen)

    def events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            self.scene_manager.handle_event(event)

    def update(self):

        self.scene_manager.update()

    def draw(self):

        self.scene_manager.draw()

        pygame.display.flip()

    async def run(self):

        while self.running:

            self.events()

            self.update()

            self.draw()

            self.clock.tick(FPS)

            await asyncio.sleep(0)

        pygame.quit()

        sys.exit()


async def main():

    game = Game()

    await game.run()


if __name__ == "__main__":

    asyncio.run(main())