import os
import math
import pygame

from settings import *


class RoomManager:

    def __init__(self):
        self.black_background = pygame.image.load(
            os.path.join(os.path.dirname(__file__), "BlackScreen.png")
        ).convert()
        self.black_background = pygame.transform.scale(
            self.black_background,
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        self.living_room_background, self.living_room_rect = self._load_room("LivingRoom.PNG")
        self.upstair_background, self.upstair_rect = self._load_room("Upstair.PNG")
        self.checking_eli_background, _ = self._load_room("CheckingEli.PNG")
        self.checking_eli2_background, _ = self._load_room("CheckingEli2.PNG")
        self.door_open_background, _ = self._load_room("DoorOpen.PNG")
        self.scary_eli_background, _ = self._load_room("ScaryEli.PNG")
        self.eli_fell_background, _ = self._load_room("EliFell.png")
        self.bedroom_background, _ = self._load_room("Bedroom.PNG")
        self.to_be_continue_image = self._load_image("Tobecontinue.png", alpha=True)

        self.current_background = self.black_background
        self.living_room_transition = False
        self.living_room_transition_start = None
        self.living_room_transition_duration = 2000
        self.returned_to_living_room = False
        self.has_completed_living_room_transition = False

        self.purple_door_rect = None
        self.white_door_rect = None
        self.living_room_door_rects_created = False
        self.upstair_door_rects_created = False
        self.upstairs_arrow_hidden_by_dialogue = False
        self.upstair_arrow_hidden_by_dialogue = False

        self.moving_arrow_image = self._load_image("LivingRoomArrow.png", alpha=True)
        self.moving_arrow_scaled = None
        self.moving_arrow_rect = None
        self.show_moving_arrow = False

        self.moving_arrow2_image = self._load_image("UpstairArrow.png", alpha=True)
        self.moving_arrow2_scaled = None
        self.moving_arrow2_rect = None
        self.moving_arrow2_click_rect = None

        self.footstep_sound_1 = self._load_sound("Footstep.ogg")
        self.footstep_sound_2 = self._load_sound("Footstep2.ogg")
        self.footstep_sound_3 = self._load_sound("Footstep3.ogg")
        self.door_slam_sound = self._load_sound("DoorSlam.ogg")
        self.scary_sound = self._load_sound("Scary.ogg")
        self.flop_sound = self._load_sound("Flop.ogg")
        self.vine_boom_sound = self._load_sound("VineBoom.ogg")

        self.upstair_anchor_rx = 0.5
        self.upstair_anchor_ry = 0.95
        self.upstair_arrow_offset = 12
        self.upstair_arrow_scale_multiplier = 3.0

        self.white_door_sequence_active = False
        self.white_door_sequence_finished = False
        self.white_door_sequence_stage = None
        self.white_door_sequence_stage_end_time = 0
        self.white_door_sequence_fade_alpha = 0
        self.white_door_sequence_fade_start_time = 0
        self.white_door_sequence_fade_duration_ms = 1000
        self.white_door_sequence_extra_hold_ms = 500
        self.white_door_black_only_extra_hold_ms = 800

        self.camera_shake_active = False
        self.camera_shake_start_time = 0
        self.camera_shake_duration_ms = 420
        self.camera_shake_amplitude_px = 14
        self.camera_shake_frequency_hz = 18

        self.scary_eli_transition_active = False
        self.scary_eli_transition_start_time = 0
        self.scary_eli_transition_duration_ms = 900
        self.scary_eli_transition_alpha = 0

        self.post_scary_sequence_active = False
        self.post_scary_sequence_stage = None
        self.post_scary_sequence_stage_end_time = 0
        self.post_scary_black_before_flop_ms = 1000
        self.post_scary_black_after_flop_ms = 1000
        self.post_scary_black_requested = False

        self.eli_fell_transition_active = False
        self.eli_fell_transition_start_time = 0
        self.eli_fell_transition_duration_ms = 1800
        self.eli_fell_transition_alpha = 0
        self.eli_fell_hold_ms = 2000
        self.eli_fell_hold_end_time = 0
        self.bedroom_sequence_finished = False

        self.to_be_continue_active = False
        self.to_be_continue_finished = False
        self.to_be_continue_stage = None
        self.to_be_continue_stage_start_time = 0
        self.to_be_continue_alpha = 0
        self.to_be_continue_black_hold_ms = 3000
        self.to_be_continue_fade_in_ms = 1500
        self.to_be_continue_hold_ms = 2000
        self.to_be_continue_fade_out_ms = 1500
        self.to_be_continue_post_black_hold_ms = 2000

    def _get_centered_overlay(self, image, max_w_ratio=0.8, max_h_ratio=0.4):
        if image is None:
            return None, None

        iw, ih = image.get_size()
        if iw <= 0 or ih <= 0:
            return None, None

        max_w = int(SCREEN_WIDTH * max_w_ratio)
        max_h = int(SCREEN_HEIGHT * max_h_ratio)
        scale = min(max_w / iw, max_h / ih, 1.0)
        tw, th = int(iw * scale), int(ih * scale)
        scaled = pygame.transform.smoothscale(image, (tw, th))
        rect = scaled.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        return scaled, rect

    def _load_room(self, filename):
        path = os.path.join(os.path.dirname(__file__), filename)
        if os.path.isfile(path):
            image = pygame.image.load(path).convert()
            iw, ih = image.get_size()
            scale = min(SCREEN_WIDTH / iw, SCREEN_HEIGHT / ih)
            tw, th = int(iw * scale), int(ih * scale)
            scaled = pygame.transform.smoothscale(image, (tw, th))
            surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            surface.fill(BLACK)
            rect = scaled.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            surface.blit(scaled, rect)
            return surface, rect
        return self.black_background.copy(), None

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

    def _play_sound_and_get_duration_ms(self, sound, fallback_ms=800):
        duration_ms = fallback_ms
        if sound is not None:
            try:
                sound.play()
                duration_ms = max(duration_ms, int(sound.get_length() * 1000))
            except Exception:
                pass
        return duration_ms

    def start_living_room_transition(self):
        self.living_room_transition = True
        self.living_room_transition_start = pygame.time.get_ticks()

    def update(self):
        if self.white_door_sequence_active:
            now = pygame.time.get_ticks()
            if self.white_door_sequence_stage == "checking_eli_1":
                if now >= self.white_door_sequence_stage_end_time:
                    self.current_background = self.checking_eli2_background
                    self.white_door_sequence_stage = "checking_eli_2"
                    duration_ms = self._play_sound_and_get_duration_ms(self.footstep_sound_2)
                    self.white_door_sequence_stage_end_time = now + duration_ms + self.white_door_sequence_extra_hold_ms

            elif self.white_door_sequence_stage == "checking_eli_2":
                if now >= self.white_door_sequence_stage_end_time:
                    self.white_door_sequence_stage = "fade_to_black"
                    self.white_door_sequence_fade_alpha = 0
                    self.white_door_sequence_fade_start_time = now
                    duration_ms = self._play_sound_and_get_duration_ms(self.footstep_sound_3)
                    self.white_door_sequence_stage_end_time = (
                        now
                        + duration_ms
                        + self.white_door_sequence_extra_hold_ms
                        + self.white_door_black_only_extra_hold_ms
                    )

            elif self.white_door_sequence_stage == "fade_to_black":
                elapsed = now - self.white_door_sequence_fade_start_time
                progress = min(1.0, elapsed / max(1, self.white_door_sequence_fade_duration_ms))
                self.white_door_sequence_fade_alpha = int(progress * 255)
                if progress >= 1.0:
                    self.current_background = self.black_background
                    self.white_door_sequence_stage = "hold_black"

            elif self.white_door_sequence_stage == "hold_black":
                if now >= self.white_door_sequence_stage_end_time:
                    self.current_background = self.door_open_background
                    if self.door_slam_sound is not None:
                        try:
                            self.door_slam_sound.play()
                        except Exception:
                            pass
                    self.start_camera_shake()
                    self.white_door_sequence_active = False
                    self.white_door_sequence_finished = True
                    self.white_door_sequence_stage = None
                    self.white_door_sequence_fade_alpha = 0

        if self.camera_shake_active:
            now = pygame.time.get_ticks()
            if now - self.camera_shake_start_time >= self.camera_shake_duration_ms:
                self.camera_shake_active = False

        if self.scary_eli_transition_active:
            now = pygame.time.get_ticks()
            elapsed = now - self.scary_eli_transition_start_time
            progress = min(1.0, elapsed / max(1, self.scary_eli_transition_duration_ms))
            self.scary_eli_transition_alpha = int(progress * 255)
            if progress >= 1.0:
                self.current_background = self.scary_eli_background
                scary_duration_ms = self._play_sound_and_get_duration_ms(self.scary_sound)
                self.scary_eli_transition_active = False
                self.scary_eli_transition_alpha = 0
                self.post_scary_sequence_active = True
                self.post_scary_sequence_stage = "hold_scary_until_sound_end"
                self.post_scary_sequence_stage_end_time = now + scary_duration_ms

        if self.post_scary_sequence_active:
            now = pygame.time.get_ticks()
            if self.post_scary_sequence_stage == "hold_scary_until_sound_end":
                if now >= self.post_scary_sequence_stage_end_time:
                    self.post_scary_sequence_stage = "wait_for_dialogue_close"

            elif self.post_scary_sequence_stage == "wait_for_dialogue_close":
                if self.post_scary_black_requested:
                    self.current_background = self.black_background
                    self.post_scary_sequence_stage = "black_before_flop"
                    self.post_scary_sequence_stage_end_time = now + self.post_scary_black_before_flop_ms
                    self.post_scary_black_requested = False

            elif self.post_scary_sequence_stage == "black_before_flop":
                if now >= self.post_scary_sequence_stage_end_time:
                    self.post_scary_sequence_stage = "black_during_flop"
                    duration_ms = self._play_sound_and_get_duration_ms(self.flop_sound)
                    self.post_scary_sequence_stage_end_time = now + duration_ms

            elif self.post_scary_sequence_stage == "black_during_flop":
                if now >= self.post_scary_sequence_stage_end_time:
                    self.post_scary_sequence_stage = "black_after_flop"
                    self.post_scary_sequence_stage_end_time = now + self.post_scary_black_after_flop_ms

            elif self.post_scary_sequence_stage == "black_after_flop":
                if now >= self.post_scary_sequence_stage_end_time:
                    self.current_background = self.eli_fell_background
                    self.post_scary_sequence_stage = "eli_fell_hold"
                    self.post_scary_sequence_stage_end_time = now + self.eli_fell_hold_ms

            elif self.post_scary_sequence_stage == "eli_fell_hold":
                if now >= self.post_scary_sequence_stage_end_time:
                    self.post_scary_sequence_active = False
                    self.post_scary_sequence_stage = None
                    self.post_scary_sequence_stage_end_time = 0
                    self.eli_fell_transition_active = True
                    self.eli_fell_transition_start_time = now
                    self.eli_fell_transition_alpha = 0

        if self.eli_fell_transition_active:
            now = pygame.time.get_ticks()
            elapsed = now - self.eli_fell_transition_start_time
            progress = min(1.0, elapsed / max(1, self.eli_fell_transition_duration_ms))
            self.eli_fell_transition_alpha = int(progress * 255)
            if progress >= 1.0:
                self.current_background = self.bedroom_background
                self.eli_fell_transition_active = False
                self.eli_fell_transition_alpha = 0
                self.bedroom_sequence_finished = True

        if self.to_be_continue_active:
            now = pygame.time.get_ticks()
            if self.to_be_continue_stage == "hold_black":
                elapsed = now - self.to_be_continue_stage_start_time
                self.to_be_continue_alpha = 0
                if elapsed >= self.to_be_continue_black_hold_ms:
                    self.to_be_continue_stage = "fade_in"
                    self.to_be_continue_stage_start_time = now

            elif self.to_be_continue_stage == "fade_in":
                elapsed = now - self.to_be_continue_stage_start_time
                progress = min(1.0, elapsed / max(1, self.to_be_continue_fade_in_ms))
                self.to_be_continue_alpha = int(progress * 255)
                if progress >= 1.0:
                    self.to_be_continue_stage = "hold_text"
                    self.to_be_continue_stage_start_time = now

            elif self.to_be_continue_stage == "hold_text":
                self.to_be_continue_alpha = 255
                elapsed = now - self.to_be_continue_stage_start_time
                if elapsed >= self.to_be_continue_hold_ms:
                    self.to_be_continue_stage = "fade_out"
                    self.to_be_continue_stage_start_time = now

            elif self.to_be_continue_stage == "fade_out":
                elapsed = now - self.to_be_continue_stage_start_time
                progress = min(1.0, elapsed / max(1, self.to_be_continue_fade_out_ms))
                self.to_be_continue_alpha = int((1.0 - progress) * 255)
                if progress >= 1.0:
                    self.to_be_continue_stage = "post_black_hold"
                    self.to_be_continue_stage_start_time = now
                    self.to_be_continue_alpha = 0

            elif self.to_be_continue_stage == "post_black_hold":
                self.to_be_continue_alpha = 0
                elapsed = now - self.to_be_continue_stage_start_time
                if elapsed >= self.to_be_continue_post_black_hold_ms:
                    self.to_be_continue_active = False
                    self.to_be_continue_finished = True
                    self.to_be_continue_stage = None
                    self.to_be_continue_alpha = 0

        if self.current_background != self.living_room_background:
            self.show_moving_arrow = False
            self.moving_arrow_rect = None

        if self.current_background != self.upstair_background:
            self.moving_arrow2_scaled = None
            self.moving_arrow2_rect = None
            self.moving_arrow2_click_rect = None

        if self.current_background == self.living_room_background:
            self.returned_to_living_room = True

        if self.current_background == self.living_room_background and not self.living_room_door_rects_created:
            self._create_living_room_door_rects()

        if self.current_background == self.upstair_background and not self.upstair_door_rects_created:
            self._create_upstair_door_rects()

        if self.living_room_transition:
            elapsed = pygame.time.get_ticks() - self.living_room_transition_start
            if elapsed >= self.living_room_transition_duration:
                self.living_room_transition = False
                self.current_background = self.living_room_background
                self.has_completed_living_room_transition = True
                self.returned_to_living_room = True
                self.show_moving_arrow = False
                self.moving_arrow_rect = None

        if self.current_background == self.upstair_background and self.moving_arrow2_image is not None and self.moving_arrow2_scaled is None:
            self.create_upstair_arrow()

    def go_upstairs(self):
        self.current_background = self.upstair_background
        self.show_moving_arrow = False
        self.moving_arrow_rect = None
        self.returned_to_living_room = False
        self.upstair_arrow_hidden_by_dialogue = False
        self.white_door_sequence_active = False
        self.white_door_sequence_finished = False
        self.white_door_sequence_stage = None
        self.white_door_sequence_fade_alpha = 0
        self.scary_eli_transition_active = False
        self.scary_eli_transition_alpha = 0
        self.post_scary_sequence_active = False
        self.post_scary_sequence_stage = None
        self.post_scary_sequence_stage_end_time = 0
        self.post_scary_black_requested = False
        self.eli_fell_transition_active = False
        self.eli_fell_transition_alpha = 0
        self.eli_fell_hold_end_time = 0
        self.bedroom_sequence_finished = False
        self.purple_door_rect = None
        self.white_door_rect = None
        self.living_room_door_rects_created = False
        self._create_upstair_door_rects()
        self.create_upstair_arrow()

    def go_downstairs(self):
        self.current_background = self.living_room_background
        self.moving_arrow2_rect = None
        self.moving_arrow2_scaled = None
        self.moving_arrow2_click_rect = None
        self.upstair_arrow_hidden_by_dialogue = False
        self.white_door_sequence_active = False
        self.white_door_sequence_finished = False
        self.white_door_sequence_stage = None
        self.white_door_sequence_fade_alpha = 0
        self.scary_eli_transition_active = False
        self.scary_eli_transition_alpha = 0
        self.post_scary_sequence_active = False
        self.post_scary_sequence_stage = None
        self.post_scary_sequence_stage_end_time = 0
        self.post_scary_black_requested = False
        self.eli_fell_transition_active = False
        self.eli_fell_transition_alpha = 0
        self.eli_fell_hold_end_time = 0
        self.bedroom_sequence_finished = False
        self.returned_to_living_room = True
        self.purple_door_rect = None
        self.white_door_rect = None
        self.upstair_door_rects_created = False
        self._create_living_room_door_rects()
        self.create_living_room_arrow()

    def start_white_door_sequence(self):
        if self.current_background != self.upstair_background:
            return
        self.white_door_sequence_active = True
        self.white_door_sequence_finished = False
        self.current_background = self.checking_eli_background
        now = pygame.time.get_ticks()
        self.white_door_sequence_stage = "checking_eli_1"
        duration_ms = self._play_sound_and_get_duration_ms(self.footstep_sound_1)
        self.white_door_sequence_stage_end_time = now + duration_ms + self.white_door_sequence_extra_hold_ms
        self.white_door_sequence_fade_alpha = 0
        self.white_door_sequence_fade_start_time = 0
        self.upstair_arrow_hidden_by_dialogue = True

    def consume_white_door_sequence_finished(self):
        if not self.white_door_sequence_finished:
            return False
        self.white_door_sequence_finished = False
        return True

    def consume_bedroom_sequence_finished(self):
        if not self.bedroom_sequence_finished:
            return False
        self.bedroom_sequence_finished = False
        return True

    def start_camera_shake(self):
        self.camera_shake_active = True
        self.camera_shake_start_time = pygame.time.get_ticks()

    def start_scary_eli_transition(self):
        if self.current_background != self.door_open_background:
            return
        self.scary_eli_transition_active = True
        self.scary_eli_transition_start_time = pygame.time.get_ticks()
        self.scary_eli_transition_alpha = 0

    def start_to_be_continue_sequence(self):
        self.current_background = self.black_background
        if self.vine_boom_sound is not None:
            try:
                self.vine_boom_sound.play()
            except Exception:
                pass
        self.to_be_continue_active = True
        self.to_be_continue_finished = False
        self.to_be_continue_stage = "hold_black"
        self.to_be_continue_stage_start_time = pygame.time.get_ticks()
        self.to_be_continue_alpha = 0

    def is_to_be_continue_active(self):
        return self.to_be_continue_active

    def consume_to_be_continue_finished(self):
        if not self.to_be_continue_finished:
            return False
        self.to_be_continue_finished = False
        return True

    def request_post_scary_black_sequence(self):
        self.post_scary_black_requested = True

    def get_camera_offset_x(self):
        if not self.camera_shake_active:
            return 0

        elapsed_ms = pygame.time.get_ticks() - self.camera_shake_start_time
        if elapsed_ms >= self.camera_shake_duration_ms:
            return 0

        decay = 1.0 - (elapsed_ms / max(1, self.camera_shake_duration_ms))
        angle = 2 * math.pi * self.camera_shake_frequency_hz * (elapsed_ms / 1000.0)
        offset = math.sin(angle) * self.camera_shake_amplitude_px * decay
        return int(offset)

    def draw_sequence_overlay(self, screen, bg_offset_x=0):
        if self.white_door_sequence_active and self.white_door_sequence_stage == "fade_to_black":
            overlay = self.black_background.copy()
            overlay.set_alpha(self.white_door_sequence_fade_alpha)
            screen.blit(overlay, (bg_offset_x, 0))

        if self.scary_eli_transition_active:
            overlay = self.scary_eli_background.copy()
            overlay.set_alpha(self.scary_eli_transition_alpha)
            screen.blit(overlay, (bg_offset_x, 0))

        if self.eli_fell_transition_active:
            overlay = self.bedroom_background.copy()
            overlay.set_alpha(self.eli_fell_transition_alpha)
            screen.blit(overlay, (bg_offset_x, 0))

        if self.to_be_continue_active and self.to_be_continue_image is not None:
            overlay, rect = self._get_centered_overlay(self.to_be_continue_image)
            if overlay is not None and rect is not None:
                overlay.set_alpha(self.to_be_continue_alpha)
                screen.blit(overlay, rect)

    def create_living_room_arrow(self):
        if not self.moving_arrow_image or self.living_room_rect is None:
            self.show_moving_arrow = False
            return

        aw, ah = self.moving_arrow_image.get_size()
        anchor_rx, anchor_ry = 0.625, 0.60
        anchor_x = self.living_room_rect.left + int(self.living_room_rect.width * anchor_rx)
        anchor_y = self.living_room_rect.top + int(self.living_room_rect.height * anchor_ry)
        arrow_w = min(int(self.living_room_rect.width * 0.44), 1200)
        arrow_h = int(ah * (arrow_w / aw))
        self.moving_arrow_scaled = pygame.transform.smoothscale(self.moving_arrow_image, (arrow_w, arrow_h))
        arrow_x = anchor_x - arrow_w // 2
        arrow_y = anchor_y - arrow_h - 14
        self.moving_arrow_rect = pygame.Rect(arrow_x, arrow_y, arrow_w, arrow_h)
        self.show_moving_arrow = True

    def _create_living_room_door_rects(self):
        if self.living_room_rect is None:
            return

        door_w = int(self.living_room_rect.width * 0.16)
        door_h = int(self.living_room_rect.height * 0.30)

        purple_x = self.living_room_rect.left + int(self.living_room_rect.width * 0.08)
        purple_y = self.living_room_rect.top + int(self.living_room_rect.height * 0.52)
        self.purple_door_rect = pygame.Rect(purple_x, purple_y, door_w, door_h)

        white_x = self.living_room_rect.left + int(self.living_room_rect.width * 0.68)
        white_y = self.living_room_rect.top + int(self.living_room_rect.height * 0.42)
        self.white_door_rect = pygame.Rect(white_x, white_y, door_w, door_h)

        self.living_room_door_rects_created = True

    def _create_upstair_door_rects(self):
        if self.upstair_rect is None:
            return

        door_w = int(self.upstair_rect.width * 0.16)
        door_h = int(self.upstair_rect.height * 0.30)

        purple_x = self.upstair_rect.left + int(self.upstair_rect.width * 0.08)
        purple_y = self.upstair_rect.top + int(self.upstair_rect.height * 0.52)
        self.purple_door_rect = pygame.Rect(purple_x, purple_y, door_w, door_h)

        white_x = self.upstair_rect.left + int(self.upstair_rect.width * 0.68)
        white_y = self.upstair_rect.top + int(self.upstair_rect.height * 0.42)
        self.white_door_rect = pygame.Rect(white_x, white_y, door_w, door_h)

        self.upstair_door_rects_created = True

    def get_clicked_door(self, pos):
        if self.current_background == self.living_room_background:
            if self.purple_door_rect and self.purple_door_rect.collidepoint(pos):
                return "purple"
            if self.white_door_rect and self.white_door_rect.collidepoint(pos):
                return "white"
        elif self.current_background == self.upstair_background:
            if self.purple_door_rect and self.purple_door_rect.collidepoint(pos):
                return "purple"
            if self.white_door_rect and self.white_door_rect.collidepoint(pos):
                return "white"
        return None

    def hide_living_room_arrow_for_dialogue(self):
        if self.show_moving_arrow:
            self.show_moving_arrow = False
            self.upstairs_arrow_hidden_by_dialogue = True

    def restore_living_room_arrow_after_dialogue(self):
        if self.upstairs_arrow_hidden_by_dialogue and self.current_background == self.living_room_background:
            self.create_living_room_arrow()
            self.upstairs_arrow_hidden_by_dialogue = False

    def hide_upstair_arrow_for_dialogue(self):
        if self.current_background == self.upstair_background and self.moving_arrow2_rect is not None:
            self.upstair_arrow_hidden_by_dialogue = True

    def restore_upstair_arrow_after_dialogue(self):
        if self.current_background == self.upstair_background and self.upstair_arrow_hidden_by_dialogue:
            self.upstair_arrow_hidden_by_dialogue = False

    def create_upstair_arrow(self):
        if not self.moving_arrow2_image:
            self.moving_arrow2_scaled = None
            self.moving_arrow2_rect = None
            self.moving_arrow2_click_rect = None
            return

        aw2, ah2 = self.moving_arrow2_image.get_size()
        if self.upstair_rect is not None:
            anchor_x = self.upstair_rect.left + int(self.upstair_rect.width * self.upstair_anchor_rx)
            anchor_y = self.upstair_rect.top + int(self.upstair_rect.height * self.upstair_anchor_ry)
            arrow_w = int(aw2 * self.upstair_arrow_scale_multiplier)
            max_w = int(self.upstair_rect.width * 0.8)
            arrow_w = min(arrow_w, max_w)
            arrow_h = int(ah2 * (arrow_w / aw2))
            self.moving_arrow2_scaled = pygame.transform.smoothscale(self.moving_arrow2_image, (arrow_w, arrow_h))
            arrow_x = anchor_x - arrow_w // 2
            arrow_y = anchor_y - arrow_h - self.upstair_arrow_offset
            self.moving_arrow2_rect = pygame.Rect(arrow_x, arrow_y, arrow_w, arrow_h)
        else:
            arrow_w = int(min(int(SCREEN_WIDTH * 0.20), aw2) * self.upstair_arrow_scale_multiplier)
            arrow_w = min(arrow_w, int(SCREEN_WIDTH * 0.8))
            arrow_h = int(ah2 * (arrow_w / aw2))
            self.moving_arrow2_scaled = pygame.transform.smoothscale(self.moving_arrow2_image, (arrow_w, arrow_h))
            arrow_x = SCREEN_WIDTH // 2 - arrow_w // 2
            arrow_y = SCREEN_HEIGHT - arrow_h - self.upstair_arrow_offset
            self.moving_arrow2_rect = pygame.Rect(arrow_x, arrow_y, arrow_w, arrow_h)

        # Keep the visible arrow size unchanged, but narrow click detection horizontally
        # so door hitboxes on the sides remain easy to click.
        click_width = max(24, int(self.moving_arrow2_rect.width * 0.42))
        click_x = self.moving_arrow2_rect.centerx - click_width // 2
        self.moving_arrow2_click_rect = pygame.Rect(
            click_x,
            self.moving_arrow2_rect.top,
            click_width,
            self.moving_arrow2_rect.height,
        )

    def draw_arrows(self, screen):
        if self.show_moving_arrow and self.moving_arrow_scaled is not None and self.moving_arrow_rect is not None:
            screen.blit(self.moving_arrow_scaled, self.moving_arrow_rect.topleft)
        if (self.current_background == self.upstair_background
                and not self.upstair_arrow_hidden_by_dialogue
                and self.moving_arrow2_scaled is not None
                and self.moving_arrow2_rect is not None):
            screen.blit(self.moving_arrow2_scaled, self.moving_arrow2_rect.topleft)

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return False

        if self.show_moving_arrow and self.moving_arrow_rect is not None and self.moving_arrow_rect.collidepoint(event.pos):
            self.go_upstairs()
            return True

        if self.moving_arrow2_click_rect is not None and self.moving_arrow2_click_rect.collidepoint(event.pos):
            self.go_downstairs()
            return True

        return False
