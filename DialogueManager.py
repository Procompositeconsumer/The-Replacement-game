import os
import pygame

from settings import *
from objects.dialogue import Dialogue


class DialogueManager:

    def __init__(self):
        self.dialogue = Dialogue()
        self.dialogue_lines = [
            ("Hmm...", None, "Ruby"),
            ("She's been oddly late today...", None, "Ruby"),
            ("What could be taking her so long?", None, "Ruby"),
        ]
        self.dialogue_index = 0
        self.dialogue.visible = False
        self.entered_gameplay_time = None
        self.initial_dialogue_delay = 1800
        self.initial_dialogue_shown = False

        self.living_room_dialogue_lines = [
            ("Didn't she say that she got some serious meeting today?", None, "Ruby"),
            ("Should I go look for her?", None, "Ruby"),
        ]

        self.choice_mode = False
        self.choice_result = None
        self.choice_labels = ["No", "Yes"]
        self.cutscene_enabled = True
        self.has_completed_living_room_transition = False
        self.started_living_room_dialogue = False
        self.dialogue_context = None

        self.purple_door_dialogue_lines = [
            ("That's my room.", None, "Ruby"),
            ("Speaking of which, I haven't done my laundry today yet.", None, "Ruby"),
            ("Meh... Later", None, "Ruby"),
        ]
        self.white_door_dialogue_lines = [
            ("This is Eli's room... Let's see if she is awake", None, "Ruby"),
            ("...", None, "Ruby"),
            ("Well I guess I should do it in the hard way!", None, "Ruby"),
        ]
        self.white_door_after_open_dialogue_lines = [
            ("RISE AND SHINE MY CUTE COUCH POTATO, TODAY ISN'T YOUR...", None, "Ruby"),
            ("Sleep...D-day?", None, "Ruby"),
        ]
        self.bedroom_reveal_dialogue_lines = [
            ("Owww...", None, "???"),
            ("!?!!", None, "Ruby"),
            ("E-Eli?", None, "Ruby"),
        ]

        self.choice_images = [
            pygame.image.load(os.path.join(os.path.dirname(__file__), "ChoosingBoxL.png")).convert_alpha(),
            pygame.image.load(os.path.join(os.path.dirname(__file__), "ChoosingBoxR.png")).convert_alpha(),
        ]
        self.choice_glow_images = [
            pygame.image.load(os.path.join(os.path.dirname(__file__), "GlowL.png")).convert_alpha(),
            pygame.image.load(os.path.join(os.path.dirname(__file__), "GlowR.png")).convert_alpha(),
        ]
        self.choice_rects = []

        self.ruby_idle_image = self._load_image("RubyIdle.PNG", alpha=True)
        self.ruby_shrug_image = self._load_image("RubyShrug.png", alpha=True)
        self.ruby_confused_image = self._load_image("RubyConfused.PNG", alpha=True)
        self.eli_awake_image = self._load_image("Eli1.png", alpha=True)
        self.ruby_idle_scale = 0.325
        self.ruby_idle_offset_x = 10

        self.knocking_sound = self._load_sound("Knocking sound.ogg")
        self.white_door_waiting_for_knock = False
        self.white_door_wait_end_time = 0
        self.white_door_wait_fallback_ms = 1200
        self.white_door_post_knock_delay_ms = 600

    def _load_image(self, filename, alpha=False):
        path = os.path.join(os.path.dirname(__file__), filename)
        if not os.path.isfile(path):
            return None
        image = pygame.image.load(path)
        return image.convert_alpha() if alpha else image.convert()

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

    def _start_white_door_knock_wait(self):
        wait_ms = self.white_door_wait_fallback_ms
        if self.knocking_sound is not None:
            try:
                self.knocking_sound.play()
                wait_ms = max(wait_ms, int(self.knocking_sound.get_length() * 1000))
            except Exception:
                pass

        wait_ms += self.white_door_post_knock_delay_ms

        self.white_door_waiting_for_knock = True
        self.white_door_wait_end_time = pygame.time.get_ticks() + wait_ms
        self.dialogue.visible = False

    def _clear_white_door_knock_wait(self):
        self.white_door_waiting_for_knock = False
        self.white_door_wait_end_time = 0

    def _show_current_dialogue(self):
        text, portrait, name = self.dialogue_lines[self.dialogue_index]
        self.dialogue.show(text, portrait, name)

    def start_living_room_dialogue(self):
        self._clear_white_door_knock_wait()
        self.dialogue_lines = self.living_room_dialogue_lines
        self.dialogue_index = 0
        self.choice_mode = False
        self.choice_result = None
        self.dialogue.visible = True
        self.dialogue.text = ""
        self.dialogue.typing_index = 0
        self.dialogue_context = "living_room"
        self._show_current_dialogue()

    def start_purple_door_dialogue(self):
        self._clear_white_door_knock_wait()
        self.dialogue_lines = self.purple_door_dialogue_lines
        self.dialogue_index = 0
        self.choice_mode = False
        self.choice_result = None
        self.dialogue.visible = True
        self.dialogue.text = ""
        self.dialogue.typing_index = 0
        self.started_living_room_dialogue = True
        self.initial_dialogue_shown = True
        self.dialogue_context = "purple"
        self._show_current_dialogue()

    def start_white_door_dialogue(self):
        self._clear_white_door_knock_wait()
        self.dialogue_lines = self.white_door_dialogue_lines
        self.dialogue_index = 0
        self.choice_mode = False
        self.choice_result = None
        self.dialogue.visible = True
        self.dialogue.text = ""
        self.dialogue.typing_index = 0
        self.started_living_room_dialogue = True
        self.initial_dialogue_shown = True
        self.dialogue_context = "white"
        self._show_current_dialogue()

    def start_white_door_after_open_dialogue(self):
        self._clear_white_door_knock_wait()
        self.dialogue_lines = self.white_door_after_open_dialogue_lines
        self.dialogue_index = 0
        self.choice_mode = False
        self.choice_result = None
        self.dialogue.visible = True
        self.dialogue.text = ""
        self.dialogue.typing_index = 0
        self.dialogue_context = "white_after_open"
        self._show_current_dialogue()

    def start_bedroom_reveal_dialogue(self):
        self._clear_white_door_knock_wait()
        self.dialogue_lines = self.bedroom_reveal_dialogue_lines
        self.dialogue_index = 0
        self.choice_mode = False
        self.choice_result = None
        self.dialogue.visible = True
        self.dialogue.text = ""
        self.dialogue.typing_index = 0
        self.dialogue_context = "bedroom_reveal"
        self._show_current_dialogue()

    def update(self):
        if self.white_door_waiting_for_knock:
            if pygame.time.get_ticks() >= self.white_door_wait_end_time:
                self.white_door_waiting_for_knock = False
                if (self.dialogue_context == "white"
                        and self.dialogue_index < len(self.dialogue_lines) - 1):
                    self.dialogue_index += 1
                self.dialogue.visible = True
                self._show_current_dialogue()
        self.dialogue.update()

    def update_initial(self, current_time, room_manager):
        if self.entered_gameplay_time is None:
            self.entered_gameplay_time = current_time
        elif (not self.dialogue.visible and not room_manager.living_room_transition
                and not self.choice_mode and not self.initial_dialogue_shown
                and not self.started_living_room_dialogue):
            if current_time - self.entered_gameplay_time >= self.initial_dialogue_delay:
                self._show_current_dialogue()
                self.dialogue.visible = True
                self.initial_dialogue_shown = True
                self.dialogue_context = "initial"

        if room_manager.has_completed_living_room_transition:
            self.has_completed_living_room_transition = True
            if (not self.started_living_room_dialogue
                    and not self.dialogue.visible
                    and not self.choice_mode):
                self.start_living_room_dialogue()
                self.started_living_room_dialogue = True

    def handle_event(self, event, room_manager, cutscene_manager, ending_manager, ui_manager):
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return False

        if self.white_door_waiting_for_knock:
            return True

        if self.choice_mode:
            for index, rect in enumerate(self.choice_rects):
                if rect.collidepoint(event.pos):
                    self._resolve_choice(index)
                    return True
            return True

        if self.dialogue.visible:
            if self.choice_result == "Yes" and self.dialogue_index == len(self.dialogue_lines) - 1:
                full = getattr(self.dialogue, "full_text", "")
                if getattr(self.dialogue, "typing_index", 0) < len(full):
                    self.dialogue.typing_index = len(full)
                    self.dialogue.text = full
                    return True
                self.dialogue.visible = False
                return True

            if self.choice_result == "No" and self.dialogue_index == len(self.dialogue_lines) - 1:
                full = getattr(self.dialogue, "full_text", "")
                if getattr(self.dialogue, "typing_index", 0) < len(full):
                    self.dialogue.typing_index = len(full)
                    self.dialogue.text = full
                    return True
                self.dialogue.visible = False
                ending_manager.start_bad_ending(ui_manager)
                return True

            if (self.dialogue_context == "living_room"
                    and self.has_completed_living_room_transition
                    and self.choice_result is None
                    and self.dialogue_index == len(self.dialogue_lines) - 1):
                self.choice_mode = True
                self.dialogue.visible = True
                return True

            if self.dialogue_index < len(self.dialogue_lines) - 1:
                if self.dialogue_context == "white" and self.dialogue_index == 0:
                    self._start_white_door_knock_wait()
                    return True
                if self.dialogue_index == 0 and self.cutscene_enabled:
                    cutscene_manager.show_cutscene = True
                self.dialogue_index += 1
                self._show_current_dialogue()
                if (self.dialogue_context == "white_after_open"
                        and self.dialogue_index == 1):
                    room_manager.start_scary_eli_transition()
            else:
                if self.dialogue_context == "purple":
                    self.dialogue.visible = False
                    self.dialogue_context = None
                elif self.dialogue_context == "white":
                    self.dialogue.visible = False
                    self.dialogue_context = None
                    room_manager.start_white_door_sequence()
                elif self.dialogue_context == "white_after_open":
                    self.dialogue.visible = False
                    self.dialogue_context = None
                    room_manager.request_post_scary_black_sequence()
                elif self.dialogue_context == "bedroom_reveal":
                    self.dialogue.visible = False
                    self.dialogue_context = None
                    room_manager.start_to_be_continue_sequence()
                elif self.dialogue_context in ("initial", "living_room") and not self.has_completed_living_room_transition:
                    room_manager.start_living_room_transition()
                    cutscene_manager.show_cutscene = False
                    self.cutscene_enabled = False
                    self.dialogue.visible = False
                    self.dialogue_context = None
                elif self.dialogue_context == "initial":
                    self.dialogue.visible = False
                    self.dialogue_context = None
            return True

        return False

    def _resolve_choice(self, index):
        self.choice_result = self.choice_labels[index]
        self.choice_mode = False
        self.dialogue.visible = False
        if self.choice_result == "No":
            self.dialogue_lines = [
                ("Meh, I think she is just snoozing, better wait a bit.", None, "Ruby"),
            ]
        else:
            self.dialogue_lines = [
                ("Ugh... This lazy potato always makes me worry.", None, "Ruby"),
                ("I should go upstairs and take a look on her.", None, "Ruby"),
            ]
        self.dialogue_index = 0
        self.dialogue.text = ""
        self.dialogue.typing_index = 0
        self._show_current_dialogue()

    def draw(self, screen):
        if self.dialogue.visible and self.has_completed_living_room_transition and not self.choice_mode:
            if self.dialogue_context == "white_after_open":
                pass
            elif (self.dialogue_context == "bedroom_reveal"
                    and getattr(self.dialogue, "full_text", "") == "Owww..."
                    and self.eli_awake_image is not None):
                self._draw_eli_awake_icon(screen)
            elif (self.dialogue_context == "bedroom_reveal"
                    and getattr(self.dialogue, "full_text", "") in ("!?!!", "E-Eli?")
                    and self.ruby_confused_image is not None):
                self._draw_ruby_confused_icon(screen)
            elif (self.dialogue_context == "purple"
                    and getattr(self.dialogue, "full_text", "") == "Meh... Later"
                    and self.ruby_shrug_image is not None):
                self._draw_ruby_shrug_icon(screen)
            elif self.choice_result == "No" and self.ruby_shrug_image is not None:
                self._draw_ruby_shrug_icon(screen)
            elif self.ruby_idle_image is not None:
                self._draw_ruby_idle_icon(screen)
        self.dialogue.draw(screen)

    def draw_choice_screen(self, screen):
        padding = 80
        box_width = 520
        box_height = 280
        dialogue_height = DIALOG_HEIGHT + 2 * self.dialogue.text_margin
        top_y = SCREEN_HEIGHT - box_height - dialogue_height - padding - 20

        left_rect = pygame.Rect(padding, top_y, box_width, box_height)
        right_rect = pygame.Rect(SCREEN_WIDTH - box_width - padding, top_y, box_width, box_height)
        self.choice_rects = [left_rect, right_rect]

        mouse_pos = pygame.mouse.get_pos()
        hover_index = None
        for i, rect in enumerate(self.choice_rects):
            if rect.collidepoint(mouse_pos):
                hover_index = i
                break

        for i, rect in enumerate(self.choice_rects):
            if i == hover_index:
                glow_image = self.choice_glow_images[i]
                glow_w, glow_h = glow_image.get_size()
                scaled_width = int(rect.width * 1.04)
                scaled_height = int(glow_h * (scaled_width / glow_w))
                glow = pygame.transform.smoothscale(glow_image, (scaled_width, scaled_height))
                glow_x = rect.centerx - glow.get_width() // 2
                glow_y = rect.centery - glow.get_height() // 2
                screen.blit(glow, (glow_x, glow_y))

            image = self.choice_images[i]
            scaled = pygame.transform.smoothscale(image, (rect.width, rect.height))
            screen.blit(scaled, rect.topleft)
            label = pygame.font.SysFont(DEFAULT_FONT, 42, bold=True).render(
                self.choice_labels[i], True, WHITE
            )
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)

    def _draw_ruby_idle_icon(self, screen):
        try:
            box = self.dialogue.get_box_rect()
            icon_w, icon_h = self.ruby_idle_image.get_size()
            scale = self.ruby_idle_scale
            target_w = int(box.width * scale)
            target_h = int(icon_h * (target_w / icon_w))
            icon = pygame.transform.smoothscale(self.ruby_idle_image, (target_w, target_h))
            icon_x = box.right - target_w - 18 + self.ruby_idle_offset_x
            icon_y = box.top - target_h + 16
            screen.blit(icon, (icon_x, icon_y))
        except Exception:
            pass

    def _draw_ruby_shrug_icon(self, screen):
        try:
            box = self.dialogue.get_box_rect()
            icon_w, icon_h = self.ruby_shrug_image.get_size()
            scale = self.ruby_idle_scale
            target_w = int(box.width * scale)
            target_h = int(icon_h * (target_w / icon_w))
            icon = pygame.transform.smoothscale(self.ruby_shrug_image, (target_w, target_h))
            icon_x = box.right - target_w - 18 + self.ruby_idle_offset_x
            icon_y = box.top - target_h + 16
            screen.blit(icon, (icon_x, icon_y))
        except Exception:
            pass

    def _draw_eli_awake_icon(self, screen):
        try:
            box = self.dialogue.get_box_rect()
            icon_w, icon_h = self.eli_awake_image.get_size()
            scale = self.ruby_idle_scale
            target_w = int(box.width * scale)
            target_h = int(icon_h * (target_w / icon_w))
            icon = pygame.transform.smoothscale(self.eli_awake_image, (target_w, target_h))
            icon_x = box.right - target_w - 18 + self.ruby_idle_offset_x
            icon_y = box.top - target_h + 16
            screen.blit(icon, (icon_x, icon_y))
        except Exception:
            pass

    def _draw_ruby_confused_icon(self, screen):
        try:
            box = self.dialogue.get_box_rect()
            icon_w, icon_h = self.ruby_confused_image.get_size()
            scale = self.ruby_idle_scale
            target_w = int(box.width * scale)
            target_h = int(icon_h * (target_w / icon_w))
            icon = pygame.transform.smoothscale(self.ruby_confused_image, (target_w, target_h))
            icon_x = box.right - target_w - 18 + self.ruby_idle_offset_x
            icon_y = box.top - target_h + 16
            screen.blit(icon, (icon_x, icon_y))
        except Exception:
            pass
