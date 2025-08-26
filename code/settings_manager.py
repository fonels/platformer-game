import json
import pygame
from os.path import join, dirname, exists
from os import makedirs

SETTINGS_DIR = join(dirname(dirname(__file__)), 'data')
SETTINGS_FILE = join(SETTINGS_DIR, 'settings.json')

class SettingsManager:
    def __init__(self):
        self.default_settings = {
            'resolution': (1280, 720),
            'music_on': True,
            'volume_music': 0.5,
            'volume_sfx': 0.7
        }
        self.resolutions = [(800, 600), (1024, 768), (1280, 720), (1920, 1080)]

        self.settings = self.default_settings.copy()
        self.load_settings()

    def load_settings(self):
        if not exists(SETTINGS_FILE):
            makedirs(SETTINGS_DIR, exist_ok=True)

        try:
            with open(SETTINGS_FILE, 'r') as f:
                loaded_settings = json.load(f)
                for key, value in loaded_settings.items():
                    if key in self.settings:
                        if key == 'resolution' and isinstance(value, list):
                            value = tuple(value)
                        self.settings[key] = value
                if self.settings['resolution'] not in self.resolutions:
                    print(f"Invalid resolution {self.settings['resolution']}. Resetting to default.")
                    self.settings['resolution'] = self.default_settings['resolution']
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Settings file not found or corrupted: {SETTINGS_FILE}. Using default settings.")
            self.settings = self.default_settings.copy()
        self.apply_settings()

    def save_settings(self):
        if not exists(SETTINGS_DIR):
            makedirs(SETTINGS_DIR)
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except IOError as e:
            print(f"Error saving settings to {SETTINGS_FILE}: {e}")

    def apply_settings(self):
        self.apply_resolution()
        self.apply_music_settings()

    def apply_resolution(self):
        pygame.display.set_mode(self.settings['resolution'])

    def apply_music_settings(self):
        if self.settings['music_on']:
            pygame.mixer.music.set_volume(self.settings['volume_music'])
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.set_volume(0)

    @property
    def resolution(self):
        return self.settings['resolution']

    @resolution.setter
    def resolution(self, res_tuple):
        if isinstance(res_tuple, list):
            res_tuple = tuple(res_tuple)
        if res_tuple in self.resolutions:
            self.settings['resolution'] = res_tuple
            self.apply_resolution()
            self.save_settings()
        else:
            print(f"Invalid resolution {res_tuple}. Keeping current resolution.")

    @property
    def music_on(self):
        return self.settings['music_on']

    @music_on.setter
    def music_on(self, value):
        self.settings['music_on'] = bool(value)
        self.apply_music_settings()
        self.save_settings()

    @property
    def volume_music(self):
        return self.settings['volume_music']

    @volume_music.setter
    def volume_music(self, value):
        self.settings['volume_music'] = max(0.0, min(1.0, value))
        self.apply_music_settings()
        self.save_settings()

    @property
    def volume_sfx(self):
        return self.settings['volume_sfx']

    @volume_sfx.setter
    def volume_sfx(self, value):
        self.settings['volume_sfx'] = max(0.0, min(1.0, value))
        self.save_settings()