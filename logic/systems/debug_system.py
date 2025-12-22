# logic/systems/debug_system.py
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from logic.core.interfaces import IGameSystem


class DebugSystem(IGameSystem):
    def on_init(self):
        # Создаем метку для FPS
        self.fps_label = MDLabel(
            text="FPS: 0",
            pos_hint={"x": 0.02, "top": 0.98},
            size_hint=(None, None),
            size=("100dp", "40dp"),
            theme_text_color="Custom",
            text_color=(1, 0, 0, 1),  # Красный, чтобы бросалось в глаза
            font_style="Caption",
            bold=True
        )
        # Добавляем её прямо на экран приложения
        self.game.add_widget(self.fps_label)

        # Обновляем текст раз в полсекунды (чтобы не мелькало)
        Clock.schedule_interval(self.update_fps, 0.5)

    def update_fps(self, dt):
        # Clock.get_fps() возвращает средний FPS за последний период
        current_fps = Clock.get_fps()
        self.fps_label.text = f"FPS: {int(current_fps)} | ENT: {len(getattr(self.game, 'active_entities', []))}"

        # Если FPS падает ниже 30, меняем цвет на ярко-красный
        if current_fps < 30:
            self.fps_label.text_color = (1, 0, 0, 1)
        else:
            self.fps_label.text_color = (0, 1, 0, 1)  # Зеленый, если всё ок

    def on_update(self, dt):
        pass

    def on_render(self, canvas, t, zoom):
        pass
