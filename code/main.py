from level import Level
from pytmx.util_pygame import load_pygame
from support import *
from data import Data
from ui import UI
from overworld import Overworld
from text import TextSystem
from settings_manager import SettingsManager
from settings_menu import SettingsMenu

class Game:
    def __init__(self):
        pygame.init()
        self.settings_manager = SettingsManager()
        self.display_surface = pygame.display.get_surface()
        pygame.display.set_caption('Lonely Kitten')
        self.clock = pygame.time.Clock()
        self.import_assets()

        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)
        self.tmx_maps = {
            0: load_pygame(join('..', 'data', 'levels', '0.tmx')),
            1: load_pygame(join('..', 'data', 'levels', '1.tmx')),
            2: load_pygame(join('..', 'data', 'levels', '2.tmx')),
            3: load_pygame(join('..', 'data', 'levels', '3.tmx')),
        }
        self.update_sound_volumes()
        self.bg_music.play(-1)
        self.text_system = TextSystem(join('..', 'graphics', 'ui', 'Roboto-Regular.ttf'))
        self.current_stage = Overworld(self.data, self.font, self.switch_stage, self.text_system)

    def switch_stage(self, target, unlock=0):
        self.text_system.clear()
        if target == 'level':
            font = pygame.font.Font(join('..', 'graphics', 'ui', 'runescape_uf.ttf'), 40)
            level = Level(
                self.tmx_maps[self.data.current_level],
                self.level_frames,
                self.audio_files,
                self.data,
                self.switch_stage,
                self.text_system
            )
            self.current_stage = level
            if self.data.current_level == 0:
                self.text_system.add_message("Добро пожаловать в игру 'Одинокий котенок'!", 2000)
                self.text_system.add_message("Ты потерялся в большом мире. Нужно найти путь домой...", 2000)
                self.text_system.add_message("Управление: Стрелки/WASD - движение, Пробел - прыжок", 3000)
                self.text_system.add_message("Собирай монеты, избегай врагов и ищи флаг для завершения уровня", 3000)
                self.text_system.add_message("Сердечки - это твои жизни. Будь осторожен!", 2000)
        elif target == 'settings':
            font = pygame.font.Font(join('..', 'graphics', 'ui', 'Roboto-Regular.ttf'), 40)
            self.current_stage = SettingsMenu(font, self.switch_stage, self.settings_manager, self,
                                              self.update_sound_volumes)
        else:
            font = pygame.font.Font(join('..', 'graphics', 'ui', 'Roboto-Regular.ttf'), 40)
            self.text_system.add_message("Нажимай Enter для выбора уровня!", 1000)
            if unlock > 0:
                self.data.unlocked_level = max(self.data.unlocked_level, unlock)
                if self.data.unlocked_level > 3:
                    self.handle_game_complete()
                    return
            else:
                self.data.health -= 1
            self.current_stage = Overworld(self.data, font, self.switch_stage, self.text_system)
        self.update_sound_volumes()

    def import_assets(self):
        self.level_frames = {
            'flag': import_folder('..', 'graphics', 'level', 'flag'),
            'saw': import_folder('..', 'graphics', 'enemies', 'saw', 'animation'),
            'floor_spike': import_folder('..', 'graphics', 'enemies', 'floor_spikes'),
            'palms': import_sub_folders('..', 'graphics', 'level', 'palms'),
            'candle': import_folder('..', 'graphics', 'level', 'candle'),
            'window': import_folder('..', 'graphics', 'level', 'window'),
            'big_chain': import_folder('..', 'graphics', 'level', 'big_chains'),
            'small_chain': import_folder('..', 'graphics', 'level', 'small_chains'),
            'candle_light': import_folder('..', 'graphics', 'level', 'candle light'),
            'player': import_sub_folders('..', 'graphics', 'player'),
            'saw': import_folder('..', 'graphics', 'enemies', 'saw', 'animation'),
            'saw_chain': import_image('..', 'graphics', 'enemies', 'saw', 'saw_chain'),
            'helicopter': import_folder('..', 'graphics', 'level', 'helicopter'),
            'boat': import_folder('..', 'graphics', 'objects', 'boat'),
            'spike': import_image('..', 'graphics', 'enemies', 'spike_ball', 'Spiked Ball'),
            'spike_chain': import_image('..', 'graphics', 'enemies', 'spike_ball', 'spiked_chain'),
            'tooth': import_folder('..', 'graphics', 'enemies', 'tooth', 'run'),
            'shell': import_sub_folders('..', 'graphics', 'enemies', 'shell'),
            'pearl': import_image('..', 'graphics', 'enemies', 'bullets', 'pearl'),
            'items': import_sub_folders('..', 'graphics', 'items'),
            'particle': import_folder('..', 'graphics', 'effects', 'particle'),
            'water_top': import_folder('..', 'graphics', 'level', 'water', 'top'),
            'water_body': import_image('..', 'graphics', 'level', 'water', 'body'),
            'bg_tiles': import_folder_dict('..', 'graphics', 'level', 'bg', 'tiles'),
            'cloud_small': import_folder('..', 'graphics', 'level', 'clouds', 'small'),
            'cloud_large': import_image('..', 'graphics', 'level', 'clouds', 'large_cloud'),
        }
        self.font = pygame.font.Font(join('..', 'graphics', 'ui', 'runescape_uf.ttf'), 40)
        self.ui_frames = {
            'heart': import_folder('..', 'graphics', 'ui', 'heart', 'full'),
            'coin': import_image('..', 'graphics', 'ui', 'coin'),
            'heart_empty': import_folder('..', 'graphics', 'ui', 'heart', 'empty'),
            'heart_bonus': import_folder('..', 'graphics', 'ui', 'heart', 'bonus')
        }
        self.audio_files = {
            'coin': pygame.mixer.Sound(join('..', 'audio', 'coin.wav')),
            'attack': pygame.mixer.Sound(join('..', 'audio', 'attack.wav')),
            'jump': pygame.mixer.Sound(join('..', 'audio', 'jump.wav')),
            'damage': pygame.mixer.Sound(join('..', 'audio', 'damage.wav')),
            'pearl': pygame.mixer.Sound(join('..', 'audio', 'pearl.wav')),
        }
        self.bg_music = pygame.mixer.Sound(join('..', 'audio', 'starlight_city.mp3'))

    def update_sound_volumes(self):
        self.bg_music.set_volume(self.settings_manager.volume_music if self.settings_manager.music_on else 0)
        for sound in self.audio_files.values():
            sound.set_volume(self.settings_manager.volume_sfx)

    def handle_game_over(self):
        overlay = pygame.Surface(self.settings_manager.resolution, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.display_surface.blit(overlay, (0, 0))

        game_over_text = self.font.render('You lost!', True, '#f5f1de')
        restart_text = self.font.render('Press "Enter" to restart the game', True, '#f5f1de')
        go_rect = game_over_text.get_frect(
            center=(self.settings_manager.resolution[0] / 2, self.settings_manager.resolution[1] / 2 - 40))
        rs_rect = restart_text.get_frect(
            center=(self.settings_manager.resolution[0] / 2, self.settings_manager.resolution[1] / 2 + 40))

        self.display_surface.blit(game_over_text, go_rect)
        self.display_surface.blit(restart_text, rs_rect)
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False

        self.data.reset()
        self.switch_stage('overworld')

    # def check_game_over(self):
    #     if self.data.health <= 0:
    #         self.handle_game_over()

    def check_game_over(self):
        health_value = self.data.health
        is_game_over = False
        if isinstance(health_value, int):
            if health_value <= 0:
                        is_game_over = True
            elif health_value > 0:
                is_game_over = False

        if is_game_over == True:
            self.handle_game_over()

    def handle_game_complete(self):
        overlay = pygame.Surface(self.settings_manager.resolution, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.display_surface.blit(overlay, (0, 0))

        game_complete_text = self.font.render('Congrats! The game is complete!', True, '#f5f1de')
        restart_text = self.font.render('Press "Enter" to exit', True, '#f5f1de')

        gc_rect = game_complete_text.get_frect(center=(self.settings_manager.resolution[0] / 2, self.settings_manager.resolution[1] / 2 - 40))
        rs_rect = restart_text.get_frect(center=(self.settings_manager.resolution[0] / 2, self.settings_manager.resolution[1] / 2 + 40))

        self.display_surface.blit(game_complete_text, gc_rect)
        self.display_surface.blit(restart_text, rs_rect)
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    pygame.quit()
                    sys.exit()

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if hasattr(self.current_stage, 'handle_event'):
                    self.current_stage.handle_event(event)

            self.text_system.update()
            self.current_stage.run(dt)
            self.ui.update(dt)
            self.text_system.draw(self.display_surface)
            self.check_game_over()
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()