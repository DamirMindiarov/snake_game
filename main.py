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


class SnakeSurvivalApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"

        if platform != 'android':
            Window.size = (400, 890)
            Window.top = 50

        # Корневой экран
        self.root_screen = MDScreen()

        # Создаем игру
        self.game = SurvivalSnakeGame()
        self.root_screen.add_widget(self.game)

        # Слой UI (поверх игры)
        self.ui_layer = MDFloatLayout()
        self.root_screen.add_widget(self.ui_layer)

        # Запуск цикла (60 FPS)
        Clock.schedule_interval(self.game.update, 1 / 60.0)

        return self.root_screen


if __name__ == '__main__':
    SnakeSurvivalApp().run()
