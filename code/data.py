import pygame

class Data:
    def __init__(self, ui):
        self.ui = ui
        self.initial_health = 3
        self.level_times = []
        self.reset()

    def reset(self):
        self._coins = 0
        self._health = self.initial_health
        self.unlocked_level = 0
        self.current_level = 0
        if self.ui:
            self.ui.create_hearts(self._health)
            self.ui.show_coins(self._coins)

    @property
    def coins(self):
        return self._coins

    @coins.setter
    def coins(self, value):
        self._coins = value
        if self.coins >= 100:
            self.coins -= 100
            self.health += 1
        self.ui.show_coins(self.coins)

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value
        self.ui.create_hearts(value)

    def add_level_time(self, time, level):
        self.level_times.append((round(time, 2), level))

    def merge_sort(self, arr):
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid])
        right = self.merge_sort(arr[mid:])

        return self.merge(left, right)

    def merge(self, left, right):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i][0] <= right[j][0]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def sort_level_times(self):
        self.level_times = self.merge_sort(self.level_times)

    def binary_search(self, value):
        self.sort_level_times()
        left, right = 0, len(self.level_times) - 1

        while left <= right:
            mid = (left + right) // 2
            if abs(self.level_times[mid][0] - value) < 0.01:
                return mid, self.level_times[mid][1]
            elif self.level_times[mid][0] < value:
                left = mid + 1
            else:
                right = mid - 1
        return -1, None

    def get_fastest_time(self):
        self.sort_level_times()
        return self.level_times[0] if self.level_times else (None, None)