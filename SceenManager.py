from engine.splash import SplashScene
from engine.menu import MenuScene


class SceneManager:
    """
    Controls which scene is currently active.
    """

    def __init__(self, screen):

        self.screen = screen

        # Dictionary of every scene
        self.scenes = {

            "SPLASH": SplashScene(self),

            "MENU": MenuScene(self),

            # Gameplay will be added in Part 2
            #"GAMEPLAY": GameplayScene(self)

        }

        # First scene shown when game launches
        self.current_scene = self.scenes["SPLASH"]


    def change_scene(self, scene_name):
        if scene_name in self.scenes:
            self.current_scene = self.scenes[scene_name]

    def handle_event(self, event):
        self.current_scene.handle_event(event)

    def update(self):
        self.current_scene.update()

    def draw(self, screen):
        self.current_scene.draw(screen)