import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT
from timer import Timer


class TextSystem:
    def __init__(self, font_path, font_size=30):
        self.font = pygame.font.Font(font_path, font_size)
        self.messages = []
        self.current_message = None
        self.timer = Timer(2000)

    def clear(self):
        self.messages = []
        self.current_message = None
        self.timer = Timer(5000)

    def add_message(self, text, duration=2000):
        self.messages.append((text, duration))

    def update(self):
        if not self.current_message and self.messages:
            text, duration = self.messages.pop(0)
            self.current_message = text
            self.timer = Timer(duration)
            self.timer.activate()

        if self.current_message:
            self.timer.update()
            if not self.timer.active:
                self.current_message = None

    def draw(self, surface):
        if self.current_message:
            text_surf = self.font.render(self.current_message, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))

            bg_rect = text_rect.inflate(20, 10)
            bg_surf = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(bg_surf, (0, 0, 0, 180), bg_surf.get_rect(), border_radius=5)

            surface.blit(bg_surf, bg_rect)
            surface.blit(text_surf, text_rect)