import pygame

from settings import *

from objects.room import Room
from objects.inventory import Inventory
from RoomManager import RoomManager
from DialogueManager import DialogueManager
from CutsceneManager import CutsceneManager
from UIManager import UIManager
from EndingManager import EndingManager


class GameplayScene:

    def __init__(self, manager):

        self.manager = manager
        self.reset()

    def reset(self):
        self.current_room = Room(
            BACKGROUND_FOLDER + "room1.png"
        )

        self.inventory = Inventory()

        self.room_manager = RoomManager()
        self.dialogue_manager = DialogueManager()
        self.cutscene_manager = CutsceneManager()
        self.ui_manager = UIManager()
        self.ending_manager = EndingManager(self.room_manager.black_background)

        self.black_background = self.room_manager.black_background
        self.dialogue = self.dialogue_manager.dialogue

        self.pending_moving_arrow = False

    # ======================================

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.room_manager.living_room_transition:
                return

            if self.room_manager.is_to_be_continue_active():
                return

            if self.room_manager.white_door_sequence_active:
                return

            if self.ending_manager.is_active():
                if self.ui_manager.handle_return_click(event):
                    self.ending_manager.begin_return_to_menu(self.manager)
                return

            if self.dialogue_manager.handle_event(
                event,
                self.room_manager,
                self.cutscene_manager,
                self.ending_manager,
                self.ui_manager
            ):
                return

            door_click = self.room_manager.get_clicked_door(event.pos)
            if door_click is not None:
                if door_click == "purple":
                    self.dialogue_manager.start_purple_door_dialogue()
                else:
                    self.dialogue_manager.start_white_door_dialogue()
                self.room_manager.hide_living_room_arrow_for_dialogue()
                return

            if self.room_manager.handle_event(event):
                self.dialogue.visible = False
                return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            menu_scene = self.manager.scenes.get("MENU")
            if menu_scene is not None and hasattr(menu_scene, "reset_transition"):
                menu_scene.reset_transition()
            self.manager.change_scene("MENU")

        self.current_room.handle_event(
            event,
            self.inventory,
            self.dialogue
        )

    # ======================================

    def update(self):

        self.current_room.update()
        self.inventory.update()
        self.room_manager.update()
        self.dialogue_manager.update()
        self.cutscene_manager.update()

        current_time = pygame.time.get_ticks()
        self.dialogue_manager.update_initial(current_time, self.room_manager)

        if (not self.dialogue_manager.has_completed_living_room_transition
            and self.room_manager.has_completed_living_room_transition
            and not self.dialogue_manager.dialogue.visible
            and not self.dialogue_manager.choice_mode):
            self.dialogue_manager.start_living_room_dialogue()

        if (self.dialogue_manager.choice_result == "Yes"
                and self.room_manager.returned_to_living_room
                and not self.room_manager.show_moving_arrow
                and not self.pending_moving_arrow):
            if (self.dialogue_manager.dialogue_index == len(self.dialogue_manager.dialogue_lines) - 1
                    and getattr(self.dialogue, 'typing_index', 0) >= len(getattr(self.dialogue, 'full_text', ''))
                    and getattr(self.dialogue, 'text', '') == getattr(self.dialogue, 'full_text', '')):
                self.pending_moving_arrow = True

        if (self.pending_moving_arrow
                and not self.dialogue.visible
                and self.room_manager.current_background == self.room_manager.living_room_background):
            self.room_manager.create_living_room_arrow()
            self.pending_moving_arrow = False

        if (self.room_manager.upstairs_arrow_hidden_by_dialogue
                and not self.dialogue.visible
                and not self.dialogue_manager.choice_mode
                and self.room_manager.current_background == self.room_manager.living_room_background):
            self.room_manager.restore_living_room_arrow_after_dialogue()

        if (self.room_manager.current_background == self.room_manager.upstair_background
                and self.dialogue.visible):
            self.room_manager.hide_upstair_arrow_for_dialogue()

        if (self.room_manager.current_background == self.room_manager.upstair_background
                and self.room_manager.upstair_arrow_hidden_by_dialogue
                and not self.dialogue.visible
                and not self.dialogue_manager.choice_mode):
            self.room_manager.restore_upstair_arrow_after_dialogue()

        if (self.room_manager.consume_white_door_sequence_finished()
                and not self.dialogue.visible
                and not self.dialogue_manager.choice_mode):
            self.dialogue_manager.start_white_door_after_open_dialogue()

        if (self.room_manager.consume_bedroom_sequence_finished()
                and not self.dialogue.visible
                and not self.dialogue_manager.choice_mode):
            self.dialogue_manager.start_bedroom_reveal_dialogue()

        if self.room_manager.consume_to_be_continue_finished():
            menu_scene = self.manager.scenes.get("MENU")
            if menu_scene is not None and hasattr(menu_scene, "reset_transition"):
                menu_scene.reset_transition()
            self.manager.change_scene("MENU")
            return

        self.ending_manager.update(self.ui_manager)
        self.ui_manager.update()

    # ======================================

    def draw(self, screen):
        bg_offset_x = self.room_manager.get_camera_offset_x()
        screen.blit(self.room_manager.current_background, (bg_offset_x, 0))
        self.room_manager.draw_sequence_overlay(screen, bg_offset_x)

        if self.cutscene_manager.show_cutscene and not self.room_manager.living_room_transition:
            self.cutscene_manager.draw(screen)

        if self.room_manager.living_room_transition:
            elapsed = pygame.time.get_ticks() - self.room_manager.living_room_transition_start
            progress = min(elapsed / self.room_manager.living_room_transition_duration, 1.0)
            overlay = self.room_manager.living_room_background.copy()
            overlay.set_alpha(int(progress * 255))
            screen.blit(overlay, (0, 0))

        if self.dialogue_manager.choice_mode:
            self.dialogue_manager.draw_choice_screen(screen)

        self.inventory.draw(screen)
        self.dialogue_manager.draw(screen)
        self.room_manager.draw_arrows(screen)

        self.ending_manager.draw(screen)
        self.ui_manager.draw(screen)

