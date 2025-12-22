# game.py
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, PushMatrix, PopMatrix, Translate, Scale
from kivy.core.window import Window
import time

from logic.core.system_manager import SystemManager
from logic.systems.InteractionSystem import InteractionSystem
from logic.systems.debug_system import DebugSystem
from logic.systems.fx_system import FXSystem
from logic.systems.mutation_dash import MutationDashSystem
from logic.systems.mutation_snap import MutationSnapSystem
from logic.systems.nature_system import NatureSystem
from logic.systems.stone_system import StoneSystem

# Импорты будущих систем (создадим их в следующих шагах)
from logic.systems.world_system import WorldSystem
from logic.systems.snake_system import SnakeSystem


class SurvivalSnakeGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Общий стейт (Shared Data)
        self.world_x, self.world_y = 0.0, 0.0
        self.target_x, self.target_y = 0.0, 0.0
        self.camera_zoom = 0.6
        self.is_touching = False
        self.touch_screen_pos = [0.0, 0.0]
        self.biomass_points = 0
        self.damage_timer = 0.0

        # КРИТИЧНО: Словарь мутаций должен быть здесь!
        self.mutations = {
            "predatory_snap": False,
            "dash": False
        }


        # Менеджер систем
        self.manager = SystemManager(self)

        # РЕГИСТРАЦИЯ СИСТЕМ (Пока закомментировано, добавим по одной)
        self.world = self.manager.register(WorldSystem(self))
        self.interaction = self.manager.register(InteractionSystem(self))

        self.stones = self.manager.register(StoneSystem(self))  # Камни теперь тут
        self.nature = self.manager.register(NatureSystem(self))  # Деревья тут

        self.fx = self.manager.register(FXSystem(self))
        self.snake = self.manager.register(SnakeSystem(self))
        self.debug = self.manager.register(DebugSystem(self))

        # ПОДКЛЮЧЕНИЕ МУТАЦИИ
        self.dash_mutation = self.manager.register(MutationDashSystem(self))
        # self.snap_mut = self.manager.register(MutationSnapSystem(self))

    def update(self, dt):
        self.manager.update_all(dt)
        self.draw_canvas()

    def draw_canvas(self):
        self.canvas.clear()
        t = time.time()

        # 1. Фоновая заливка (экранные координаты)
        with self.canvas:
            Color(0.18, 0.28, 0.18, 1)
            Rectangle(pos=(0, 0), size=(Window.width, Window.height))

        # 2. Мировой рендеринг (координаты игры)
        with self.canvas:
            PushMatrix()
            # Центрируем камеру на игроке
            Translate(Window.width / 2, Window.height / 2, 0)
            Scale(self.camera_zoom, self.camera_zoom, 1)
            Translate(-self.world_x, -self.world_y, 0)

            # А. Отрисовка всех стандартных систем:
            # Слой 0 мира (камни, стволы), еда, эффекты, змея
            self.manager.render_all(self.canvas, t, self.camera_zoom)

            # Б. Отрисовка верхнего слоя (кроны деревьев):
            # Вызываем метод напрямую у WorldSystem, чтобы он перекрыл змею
            if hasattr(self, 'world'):
                self.world.draw_upper_layer(self.canvas)

            PopMatrix()

    def on_touch_down(self, touch):
        # 1. UI логика (оставляем тут, так как это уровень приложения)
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if hasattr(app, 'game_ui') and app.game_ui.is_menu_open():
            if touch.x > Window.width / 2: app.game_ui.toggle_menu()
            return True

        # 2. Обновляем общее состояние
        self.is_touching = True
        self.touch_screen_pos = [touch.x, touch.y]

        # 3. ТРАНСЛЯЦИЯ СОБЫТИЯ В СИСТЕМЫ
        self.manager.post_event('on_touch_down', touch)
        return True

    def on_touch_move(self, touch):
        if self.is_touching:
            self.touch_screen_pos = [touch.x, touch.y]
            # ТРАНСЛЯЦИЯ
            self.manager.post_event('on_touch_move', touch)
        return True

    def on_touch_up(self, touch):
        self.is_touching = False
        # ТРАНСЛЯЦИЯ
        self.manager.post_event('on_touch_up', touch)
        return True
