# logic/systems/mutation_snap.py
import math
import time
from logic.core.mutations import IMutationSystem


class MutationSnapSystem(IMutationSystem):
    @property
    def mutation_id(self):
        # Должно совпадать с ключом в self.mutations в game.py
        return "predatory_snap"

    def on_init(self):
        self.snap_radius = 150.0  # Дальность "зрения" змеи
        self.snap_power = 15.0  # Скорость полета к мыши
        self.game.snap_timer = 0.0  # Время активного прыжка
        self.snap_direction = [0.0, 0.0]
        self.cooldown = 0.0

    def on_update(self, dt):
        # 1. Проверка активности мутации (из базового класса)
        if not self.is_active():
            return

        # 2. Обработка кулдауна
        if self.cooldown > 0:
            self.cooldown -= dt

        # 3. ЛОГИКА ПОИСКА ЦЕЛИ (только если не летим прямо сейчас)
        if self.game.snap_timer <= 0:
            if self.cooldown <= 0:
                self._find_target()
        else:
            # 4. ЛОГИКА ПОЛЕТА (если прыжок активен)
            self._apply_snap_movement(dt)

    def _find_target(self):
        hx, hy = self.game.world_x, self.game.world_y
        target = None
        min_dist_sq = self.snap_radius ** 2

        # Ищем в списке активных сущностей
        entities = getattr(self.game, 'active_entities', [])
        for ent in entities:
            # Прыгаем только на живых существ с флагом добычи
            if not ent.alive or not getattr(ent, 'is_prey', True):
                continue

            # Считаем расстояние по осям (индексы 0 и 1 для списка)
            ex, ey = ent.pos[0], ent.pos[1]
            dx, dy = ex - hx, ey - hy
            d2 = dx * dx + dy * dy

            if d2 < min_dist_sq:
                min_dist_sq = d2
                target = ent

        if target:
            self._activate_snap(target)

    def _activate_snap(self, target):
        hx, hy = self.game.world_x, self.game.world_y
        dx = target.pos[0] - hx
        dy = target.pos[1] - hy
        dist = math.sqrt(dx * dx + dy * dy)

        if dist > 5:
            # Устанавливаем вектор направления строго К цели
            self.snap_direction = [dx / dist, dy / dist]
            self.game.snap_timer = 0.22  # Длительность выпада
            self.cooldown = 0.7  # Перезарядка

            # Сбрасываем инерцию для резкого старта (как в Dash)
            self.game.vel_x, self.game.vel_y = 0.0, 0.0

    def _apply_snap_movement(self, dt):
        self.game.snap_timer -= dt

        # Сила перемещения (как dash_power)
        move_x = self.snap_direction[0] * self.snap_power
        move_y = self.snap_direction[1] * self.snap_power

        # Проверка коллизий через WorldSystem (копия логики из твоего Dash)
        world = getattr(self.game, 'world', None)
        if world:
            if not world.is_tile_solid(self.game.world_x + move_x, self.game.world_y):
                self.game.world_x += move_x
            if not world.is_tile_solid(self.game.world_x, self.game.world_y + move_y):
                self.game.world_y += move_y

        # Обновляем хвост сразу, чтобы он не отставал при рывке
        snake_sys = self.game.manager.get_system('SnakeSystem')
        if snake_sys:
            snake_sys._update_tail()

    def on_render(self, canvas, t, zoom):
        pass
