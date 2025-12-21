import os
from kivy.config import Config

from logic.physics import SnakePhysicsMixin
from logic.renderer import GameRendererMixin

# Настройки окна для ПК (имитация POCO X7 Pro)
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '890')
Config.set('graphics', 'resizable', False)

from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.utils import platform


# --- КЛАСС ИГРЫ ---
class SurvivalSnakeGame(Widget, GameRendererMixin, SnakePhysicsMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Базовые переменные (физика и мир)
        self.world_x, self.world_y = 0, 0
        self.target_x, self.target_y = 0, 0
        self.is_touching = False
        self.touch_screen_pos = [0, 0]

        # Инициализируем переменные из миксина физики
        self.init_physics()

        # Заглушки для будущих систем
        self.camera_zoom = 1.0

    def update(self, dt):
        # Если координаты меняются в консоли — значит физика работает!
        print(f"X: {int(self.world_x)} Y: {int(self.world_y)}")
        # 1. Логика управления
        if self.is_touching:
            zoom = self.camera_zoom
            rel_x = self.touch_screen_pos[0] - Window.width / 2
            rel_y = self.touch_screen_pos[1] - Window.height / 2
            self.target_x = self.world_x + (rel_x / zoom)
            self.target_y = self.world_y + (rel_y / zoom)

        # 2. Здесь будут вызовы систем: move_head(), check_collisions() и т.д.
        self.apply_inertia()

        # 3. Отрисовка (пока заглушка)
        self.draw_canvas()

    # def draw_canvas(self):
    #     # Метод будет наполнен через GameRendererMixin
    #     pass

    def on_touch_down(self, touch):
        self.is_touching = True
        self.touch_screen_pos = [touch.x, touch.y]
        return True # ВАЖНО: сообщает системе, что нажатие обработано здесь

    def on_touch_move(self, touch):
        self.touch_screen_pos = [touch.x, touch.y]
        return True

    def on_touch_up(self, touch):
        self.is_touching = False


# --- ГЛАВНОЕ ПРИЛОЖЕНИЕ ---
class SnakeSurvivalApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"

        # Центрируем окно на ПК
        if platform != 'android':
            Window.size = (400, 890)
            Window.top = 50

        # Корневой экран
        self.root_screen = MDScreen()

        # Слой 1: Игра
        self.game = SurvivalSnakeGame()
        self.root_screen.add_widget(self.game)

        # Слой 2: UI (поверх игры)
        self.ui_layer = MDFloatLayout()
        self.root_screen.add_widget(self.ui_layer)

        # Запуск игрового цикла (60 FPS)
        Clock.schedule_interval(self.game.update, 1 / 60.0)

        return self.root_screen


if __name__ == '__main__':
    SnakeSurvivalApp().run()
