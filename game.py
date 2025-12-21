# game.py
from kivy.uix.widget import Widget
from kivy.core.window import Window

from logic.collisions import CollisionMixin
# Импортируем все наши миксины
from logic.renderer import GameRendererMixin
from logic.physics import SnakePhysicsMixin
from logic.snake_movement import SnakeMovementMixin
from logic.engine.game_loop import GameLoopMixin
from logic.world_map import WorldMapMixin


class SurvivalSnakeGame(Widget, GameRendererMixin, SnakePhysicsMixin,
                        SnakeMovementMixin, GameLoopMixin, WorldMapMixin, CollisionMixin ):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Инициализация систем
        self.init_physics()
        self.init_snake_data()

        # Базовые параметры
        self.world_x, self.world_y = 0.0, 0.0
        self.target_x, self.target_y = 0.0, 0.0
        self.is_touching = False
        self.touch_screen_pos = [0.0, 0.0]
        self.camera_zoom = 0.6

        # Параметры бури (для будущего)
        self.storm_alpha = 0.0
        self.storm_phase = "idle"

        self.init_world_map()

    def on_touch_down(self, touch):
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
