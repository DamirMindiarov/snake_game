# logic/engine/game_loop.py

class GameLoopMixin:
    def update(self, dt):
        """Главный диспетчер игрового цикла"""

        print(self.obstacles.keys())

        # 1. Фаза ввода (Управление)
        self._process_input()

        # 2. Фаза физики и движения
        self._process_movement(dt)

        # 3. Фаза мира и событий (Буря, Еда, Коллизии)
        self._process_world_events(dt)

        # 4. Фаза рендеринга
        self.draw_canvas()

    def _process_input(self):
        """Расчет цели на основе тача и зума"""
        if getattr(self, 'is_touching', False):
            from kivy.core.window import Window
            zoom = getattr(self, 'camera_zoom', 1.0)

            # Центрируем экранные координаты
            rel_x = self.touch_screen_pos[0] - Window.width / 2
            rel_y = self.touch_screen_pos[1] - Window.height / 2

            # Устанавливаем цель в мировых координатах
            self.target_x = self.world_x + (rel_x / zoom)
            self.target_y = self.world_y + (rel_y / zoom)

    def _process_movement(self, dt):
        """Движение всех физических объектов"""
        if hasattr(self, 'apply_inertia'):
            self.apply_inertia()

        if hasattr(self, 'move_tail'):
            self.move_tail()

    def _process_world_events(self, dt):
        """Обработка игровых событий"""
        self.check_map_generation()
        pass
