from settings import *
from sprites import AnimatedSprite
from timer import Timer

class UI:
    def __init__(self, font, frames):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.font = font

        self.heart_frames = frames['heart']
        self.heart_empty_frames = frames['heart_empty']
        self.heart_bonus_frames = frames['heart_bonus']

        self.heart_surf_width = self.heart_frames[0].get_width()
        self.heart_padding = 3
        self.base_hearts_count = 3

        self.coin_amount = 0
        self.coin_timer = Timer(1000)
        self.coin_surf = frames['coin']

    def create_hearts(self, current_health):
        for sprite in self.sprites:
            sprite.kill()

        num_base_hearts = min(current_health, self.base_hearts_count)
        num_bonus_hearts = max(0, current_health - self.base_hearts_count)

        for i in range(self.base_hearts_count):
            x = 10 + i * (self.heart_surf_width + self.heart_padding)
            y = 10
            if i < num_base_hearts:
                Heart((x, y), self.heart_frames, self.sprites, 'full')
            else:
                Heart((x, y), self.heart_empty_frames, self.sprites, 'empty')

        for i in range(num_bonus_hearts):
            x = 10 + (self.base_hearts_count + i) * (self.heart_surf_width + self.heart_padding) + 15
            y = 10
            Heart((x, y), self.heart_bonus_frames, self.sprites, 'bonus')

    def display_text(self):
        if self.coin_timer.active:
            text_surf = self.font.render(str(self.coin_amount), False, '#33323d')
            text_rect = text_surf.get_frect(topleft=(16, 34))
            self.display_surface.blit(text_surf, text_rect)

            coin_rect = self.coin_surf.get_frect(center=text_rect.bottomleft).move(0, -6)
            self.display_surface.blit(self.coin_surf, coin_rect)

    def show_coins(self, amount):
        self.coin_amount = amount
        self.coin_timer.activate()

    def update_display(self, resolution):
        self.display_surface = pygame.display.get_surface()
        if hasattr(self, 'sprites'):
            for sprite in self.sprites:
                sprite.kill()
            self.create_hearts(len(self.sprites))

    def update(self, dt):
        self.coin_timer.update()
        self.sprites.update(dt)
        self.sprites.draw(self.display_surface)
        self.display_text()

class Heart(AnimatedSprite):
    def __init__(self, pos, frames, groups, heart_type='full'):
        animation_speed_for_type = ANIMATION_SPEED if heart_type == 'full' else 0
        super().__init__(pos, frames, groups, animation_speed=animation_speed_for_type)

        self.active = False
        self.heart_type = heart_type

        self.frame_index = 0

    def update(self, dt):
        if self.heart_type == 'full':
            super().update(dt)