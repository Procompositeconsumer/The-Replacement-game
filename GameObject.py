import pygame


class GameObject:

    def __init__(
        self,
        name,
        image_path,
        x,
        y,

        description="",

        visible=True,

        enabled=True,

        interactable=True,

        pickable=False,

        useable=False,

        collectible=False,

        examine_text=None,

        hover_text=None
    ):

        self.name = name

        self.description = description

        self.pickable = pickable

        self.useable = useable

        self.collectible = collectible

        self.visible = visible

        self.enabled = enabled

        self.interactable = interactable

        self.hover = False

        self.examine_text = examine_text

        self.hover_text = hover_text

        # -----------------------------

        self.image = pygame.image.load(
            image_path
        ).convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.topleft = (x, y)

    # ===========================================

    def update(self):

        if not self.visible:
            return

        mouse = pygame.mouse.get_pos()

        self.hover = self.rect.collidepoint(mouse)

    # ===========================================

    def draw(self, screen):

        if not self.visible:
            return

        screen.blit(self.image, self.rect)

    # ===========================================

    def handle_event(
        self,
        event,
        inventory,
        dialogue
    ):

        if not self.visible:
            return

        if not self.enabled:
            return

        if not self.interactable:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                if self.rect.collidepoint(event.pos):

                    self.interact(
                        inventory,
                        dialogue
                    )

    # ===========================================

    def interact(
        self,
        inventory,
        dialogue
    ):
        """
        Default interaction.
        """

        if self.pickable:

            inventory.add(self)

            self.hide()

            dialogue.show(
                f"You picked up the {self.name}."
            )

            return

        if self.description != "":

            dialogue.show(
                self.description
            )

    # ===========================================

    def examine(self, dialogue):

        if self.examine_text:

            dialogue.show(
                self.examine_text
            )

        elif self.description:

            dialogue.show(
                self.description
            )

    # ===========================================

    def use(
        self,
        target,
        dialogue
    ):
        """
        Override later for puzzle logic.
        """
        dialogue.show(
            "Nothing happened."
        )

    # ===========================================

    def hide(self):

        self.visible = False

    # ===========================================

    def show(self):

        self.visible = True

    # ===========================================

    def enable(self):

        self.enabled = True

    # ===========================================

    def disable(self):

        self.enabled = False