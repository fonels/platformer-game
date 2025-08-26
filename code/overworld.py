from settings import *

class Overworld:
    def __init__(self, data, font, switch_stage, text_system):
        self.display_surface = pygame.display.get_surface()
        self.data = data
        self.switch_stage = switch_stage
        self.text_system = text_system

        self.font = font
        self.num_levels = 4
        self.num_options = self.num_levels + 2
        self.selection_index = self.data.current_level
        self.selection_cooldown = 200
        self.last_selection_time = 0
        self.search_input = ""
        self.search_active = False
        self.show_fastest = False

        self.colors = {
            'highlight': '#f5f1de',
            'available': '#ddc6a1',
            'locked': '#a09384',
            'strikethrough': '#c2474b'
        }

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            current_time = pygame.time.get_ticks()
            if self.search_active:
                if event.key == pygame.K_RETURN:
                    self.perform_time_search()
                    self.search_active = False
                    self.search_input = ""
                    self.last_selection_time = current_time
                elif event.key == pygame.K_BACKSPACE:
                    self.search_input = self.search_input[:-1]
                elif event.unicode.isdigit() or event.unicode == '.':
                    self.search_input += event.unicode
            elif current_time - self.last_selection_time > self.selection_cooldown:
                if event.key == pygame.K_DOWN:
                    self.selection_index = (self.selection_index + 1) % self.num_options
                    self.last_selection_time = current_time
                elif event.key == pygame.K_UP:
                    self.selection_index = (self.selection_index - 1 + self.num_options) % self.num_options
                    self.last_selection_time = current_time
                elif event.key == pygame.K_RETURN:
                    if self.selection_index < self.num_levels:
                        if self.selection_index <= self.data.unlocked_level:
                            self.data.current_level = self.selection_index
                            self.switch_stage('level')
                    elif self.selection_index == self.num_levels:
                        self.switch_stage('settings')
                    elif self.selection_index == self.num_levels + 1:
                        self.search_active = True
                        self.show_fastest = False
                        self.last_selection_time = current_time
                elif event.key == pygame.K_f:
                    self.show_fastest = True
                    self.search_active = False
                    self.search_input = ""
                    self.last_selection_time = current_time

    def perform_time_search(self):
        try:
            value = float(self.search_input)
            index, level = self.data.binary_search(value)
            if index >= 0:
                self.text_system.add_message(f"Время {value:.2f}s найдено на Level {level + 1}!", 2000)
            else:
                self.text_system.add_message(f"Время {value:.2f}s не найдено", 2000)
        except ValueError:
            self.text_system.add_message("Некорректный ввод. Введите число.", 2000)

    def draw(self):
        self.display_surface.fill('#92a9ce')

        title_surf = self.font.render('SELECT LEVEL', True, self.colors['highlight'])
        title_rect = title_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4))
        self.display_surface.blit(title_surf, title_rect)

        item_height = 60
        start_y = WINDOW_HEIGHT / 2.5
        level_names = ['First Crush', 'Second Wind', 'Third Try', 'Last Fight']
        for i in range(self.num_levels):
            text = f"Level {i+1} ({level_names[i]})"
            is_completed = i < self.data.unlocked_level
            is_unlocked = i <= self.data.unlocked_level
            is_selected = i == self.selection_index

            if not is_unlocked:
                color = self.colors['locked']
            elif is_selected:
                color = self.colors['highlight']
            else:
                color = self.colors['available']

            item_surf = self.font.render(text, True, color)
            item_rect = item_surf.get_frect(center=(WINDOW_WIDTH / 2, start_y + i * item_height))
            self.display_surface.blit(item_surf, item_rect)

            if is_completed:
                line_start = (item_rect.left, item_rect.centery)
                line_end = (item_rect.right, item_rect.centery)
                pygame.draw.line(self.display_surface, self.colors['strikethrough'], line_start, line_end, 4)

        settings_text = "Settings"
        is_selected = self.selection_index == self.num_levels
        color = self.colors['highlight'] if is_selected else self.colors['available']
        settings_surf = self.font.render(settings_text, True, color)
        settings_rect = settings_surf.get_frect(center=(WINDOW_WIDTH / 2, start_y + self.num_levels * item_height))
        self.display_surface.blit(settings_surf, settings_rect)

        times_text = "Level Times"
        is_selected = self.selection_index == self.num_levels + 1
        color = self.colors['highlight'] if is_selected else self.colors['available']
        times_surf = self.font.render(times_text, True, color)
        times_rect = times_surf.get_frect(center=(WINDOW_WIDTH / 2, start_y + (self.num_levels + 1) * item_height))
        self.display_surface.blit(times_surf, times_rect)

        if self.data.level_times:
            self.data.sort_level_times()
            if self.show_fastest:
                fastest_time, level = self.data.get_fastest_time()
                times_text = f"Fastest Time: {fastest_time:.2f}s (Level {level + 1})"
            else:
                times_text = f"Sorted Times: {', '.join(f'L{level + 1}: {time:.2f}s' for time, level in self.data.level_times)}"
            times_surf = self.font.render(times_text, True, self.colors['available'])
            times_rect = times_surf.get_frect(center=(WINDOW_WIDTH / 2, start_y + (self.num_levels + 2) * item_height))
            self.display_surface.blit(times_surf, times_rect)

        if self.search_active:
            search_text = f"Enter time to search (seconds): {self.search_input}"
            search_surf = self.font.render(search_text, True, self.colors['highlight'])
            search_rect = search_surf.get_frect(center=(WINDOW_WIDTH / 2, start_y + (self.num_levels + 3) * item_height))
            self.display_surface.blit(search_surf, search_rect)

        if self.data.current_level == 0 and not hasattr(self, 'intro_shown'):
            self.text_system.add_message("Ты - маленький котенок, потерявшийся в большом городе...", 1000)
            self.text_system.add_message("Нужно пройти все уровни, чтобы найти дорогу домой", 1000)
            self.text_system.add_message("Нажимай Enter!", 1000)
            self.text_system.add_message("Добро пожаловать в игру 'Одинокий котенок'!", 2000)
            self.text_system.add_message("Ты потерялся в большом мире. Нужно найти путь домой...", 2000)
            self.text_system.add_message("Управление: Стрелки/WASD - движение, Пробел - прыжок", 3000)
            self.text_system.add_message("Собирай монеты, избегай врагов и ищи флаг для завершения уровня", 3000)
            self.text_system.add_message("Сердечки - это твои жизни. Будь осторожен!", 2000)
            self.intro_shown = True

    def run(self, dt):
        self.draw()