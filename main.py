# main.py
from kivy.config import Config

# Настройки окна для имитации мобильного устройства
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '890')
Config.set('graphics', 'resizable', False)

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.window import Window

# Импортируем наш класс игры из нового файла
from game import SurvivalSnakeGame

# main.py
from interface.menu_drawer import GameInterfaceManager


class SnakeSurvivalApp(MDApp):
    def build(self):
        # ... настройки темы и окна ...
        self.root_screen = MDScreen()

        # 1. Инициализируем игру
        self.game = SurvivalSnakeGame()
        self.root_screen.add_widget(self.game)

        # 2. Инициализируем интерфейс
        self.ui_manager = GameInterfaceManager()
        self.ui_manager.setup_ui(self.root_screen)

        # Приложение запоминает состояние для игры
        self.game_ui = self.ui_manager

        Clock.schedule_interval(self.game.update, 1 / 60.0)
        return self.root_screen


if __name__ == '__main__':
    SnakeSurvivalApp().run()
