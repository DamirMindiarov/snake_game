# game.py
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, PushMatrix, PopMatrix, Translate, Scale
from kivy.core.window import Window
import time

from logic.core.system_manager import SystemManager
from logic.systems.fx_system import FXSystem
from logic.systems.mutation_dash import MutationDashSystem
from logic.systems.mutation_snap import MutationSnapSystem

# Импорты будущих систем (создадим их в следующих шагах)
from logic.systems.world_system import WorldSystem
from logic.systems.snake_system import SnakeSystem
from logic.systems.biomass_system import BiomassSystem

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
        self.fx = self.manager.register(FXSystem(self))
        self.snake = self.manager.register(SnakeSystem(self))
        self.biomass = self.manager.register(BiomassSystem(self))


        # ПОДКЛЮЧЕНИЕ МУТАЦИИ
        self.dash_mutation = self.manager.register(MutationDashSystem(self))
        self.snap_mut = self.manager.register(MutationSnapSystem(self))

    def update(self, dt):
        self.manager.update_all(dt)
        self.draw_canvas()

    def draw_canvas(self):
        self.canvas.clear()
        t = time.time()

        # 1. Фон (теперь рисуем здесь или вынесем в BackgroundSystem)
        with self.canvas:
            Color(0.18, 0.28, 0.18, 1)
            Rectangle(pos=(0, 0), size=(Window.width, Window.height))

        # 2. Отрисовка систем в мировых координатах
        with self.canvas:
            PushMatrix()
            Translate(Window.width / 2, Window.height / 2, 0)
            Scale(self.camera_zoom, self.camera_zoom, 1)
            Translate(-self.world_x, -self.world_y, 0)

            self.manager.render_all(self.canvas, t, self.camera_zoom)

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
