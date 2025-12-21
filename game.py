# game.py
from kivy.uix.widget import Widget
from kivy.core.window import Window

from logic.collisions import CollisionMixin
from logic.food_system import FoodSystemMixin
# Импортируем все наши миксины
from logic.renderer import GameRendererMixin
from logic.physics import SnakePhysicsMixin
from logic.snake_movement import SnakeMovementMixin
from logic.engine.game_loop import GameLoopMixin
from logic.world_map import WorldMapMixin


class SurvivalSnakeGame(Widget, GameRendererMixin, SnakePhysicsMixin,
                        SnakeMovementMixin, GameLoopMixin, WorldMapMixin, CollisionMixin, FoodSystemMixin ):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.world_x, self.world_y = 0.0, 0.0
        self.target_x, self.target_y = 0.0, 0.0

        self.mutations = {
            "predatory_snap": False  # Изначально выключена
        }

        # 1. ИНИЦИАЛИЗИРУЕМ ЕДУ В ПЕРВУЮ ОЧЕРЕДЬ
        # Это создаст self.food_items и предотвратит ошибку
        self.init_food()

        # Инициализация систем
        self.init_physics()
        self.init_snake_data()

        # Базовые параметры
        self.is_touching = False
        self.touch_screen_pos = [0.0, 0.0]
        self.camera_zoom = 0.6

        # Параметры бури (для будущего)
        self.storm_alpha = 0.0
        self.storm_phase = "idle"

        self.init_world_map()

    def on_touch_down(self, touch):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()

        # Проверка через наш новый интерфейс
        if hasattr(app, 'game_ui') and app.game_ui.is_menu_open():
            # Если кликнули вне меню (в правую часть экрана) — закрываем его
            if touch.x > Window.width / 2:
                app.game_ui.toggle_menu()
            return True

        # Игнорируем зону кнопки
        if touch.x < 100 and touch.y > Window.height - 100:
            return super().on_touch_down(touch)

        self.is_touching = True
        self.touch_screen_pos = [touch.x, touch.y]
        return True

    def on_touch_move(self, touch):
        if self.is_touching:
            self.touch_screen_pos = [touch.x, touch.y]
            return True

    def on_touch_up(self, touch):
        self.is_touching = False
        return True
