import pygame
from settings import *

class SettingsMenu:
    def __init__(self, font, switch_stage, settings_manager, game, update_sound_volumes):
        self.display_surface = pygame.display.get_surface()
        self.font = font
        self.switch_stage = switch_stage
        self.settings_manager = settings_manager
        self.game = game
        self.update_sound_volumes = update_sound_volumes

        self.options = [
            {'name': 'Resolution', 'type': 'resolution'},
            {'name': 'Music', 'type': 'toggle', 'setting_key': 'music_on'},
            {'name': 'Music Volume', 'type': 'slider', 'setting_key': 'volume_music', 'min_val': 0.0, 'max_val': 1.0, 'step': 0.1},
            {'name': 'SFX Volume', 'type': 'slider', 'setting_key': 'volume_sfx', 'min_val': 0.0, 'max_val': 1.0, 'step': 0.1},
            {'name': 'Back', 'type': 'back'}
        ]
        self.selection_index = 0
        self.selection_cooldown = 200
        self.last_selection_time = 0

        self.colors = {
            'highlight': '#f5f1de',
            'available': '#ddc6a1',
            'background': '#33323d'
        }

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_selection_time > self.selection_cooldown:
                selected_option = self.options[self.selection_index]

                if event.key == pygame.K_DOWN:
                    self.selection_index = (self.selection_index + 1) % len(self.options)
                    self.last_selection_time = current_time
                elif event.key == pygame.K_UP:
                    self.selection_index = (self.selection_index - 1) % len(self.options)
                    self.last_selection_time = current_time
                elif event.key == pygame.K_RETURN:
                    if selected_option['type'] == 'back':
                        self.switch_stage('overworld')
                    elif selected_option['type'] == 'toggle':
                        current_value = getattr(self.settings_manager, selected_option['setting_key'])
                        setattr(self.settings_manager, selected_option['setting_key'], not current_value)
                        self.update_sound_volumes()
                        self.last_selection_time = current_time

                elif event.key == pygame.K_RIGHT:
                    if selected_option['type'] == 'resolution':
                        current_res = self.settings_manager.resolution
                        current_index = self.settings_manager.resolutions.index(current_res)
                        next_index = (current_index + 1) % len(self.settings_manager.resolutions)
                        self.settings_manager.resolution = self.settings_manager.resolutions[next_index]
                        self.update_display()
                        self.last_selection_time = current_time
                    elif selected_option['type'] == 'slider':
                        current_val = getattr(self.settings_manager, selected_option['setting_key'])
                        new_val = min(selected_option['max_val'], current_val + selected_option['step'])
                        setattr(self.settings_manager, selected_option['setting_key'], new_val)
                        self.update_sound_volumes()
                        self.last_selection_time = current_time

                elif event.key == pygame.K_LEFT:
                    if selected_option['type'] == 'resolution':
                        current_res = self.settings_manager.resolution
                        current_index = self.settings_manager.resolutions.index(current_res)
                        prev_index = (current_index - 1) % len(self.settings_manager.resolutions)
                        self.settings_manager.resolution = self.settings_manager.resolutions[prev_index]
                        self.update_display()
                        self.last_selection_time = current_time
                    elif selected_option['type'] == 'slider':
                        current_val = getattr(self.settings_manager, selected_option['setting_key'])
                        new_val = max(selected_option['min_val'], current_val - selected_option['step'])
                        setattr(self.settings_manager, selected_option['setting_key'], new_val)
                        self.update_sound_volumes()
                        self.last_selection_time = current_time

    def update_display(self):
        pygame.display.set_mode(self.settings_manager.resolution, pygame.RESIZABLE)
        self.display_surface = pygame.display.get_surface()
        self.game.ui.update_display(self.settings_manager.resolution)

    def display_menu(self):
        title_surf = self.font.render("Settings", True, self.colors['highlight'])
        title_rect = title_surf.get_frect(center=(self.settings_manager.resolution[0] / 2, self.settings_manager.resolution[1] / 4))
        self.display_surface.blit(title_surf, title_rect)

        item_height = 60
        start_y = self.settings_manager.resolution[1] / 2.5
        for i, option in enumerate(self.options):
            is_selected = i == self.selection_index
            color = self.colors['highlight'] if is_selected else self.colors['available']

            display_text = option['name']
            if option['type'] == 'resolution':
                display_text += f": {self.settings_manager.resolution[0]}x{self.settings_manager.resolution[1]}"
            elif option['type'] == 'toggle':
                current_value = getattr(self.settings_manager, option['setting_key'])
                display_text += f": {'On' if current_value else 'Off'}"
            elif option['type'] == 'slider':
                current_value = getattr(self.settings_manager, option['setting_key'])
                display_text += f": {int(current_value * 100)}%"

            item_surf = self.font.render(display_text, True, color)
            item_rect = item_surf.get_frect(center=(self.settings_manager.resolution[0] / 2, start_y + i * item_height))
            self.display_surface.blit(item_surf, item_rect)

    def run(self, dt):
        self.display_surface.fill(self.colors['background'])
        self.display_menu()