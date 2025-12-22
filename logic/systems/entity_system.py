from kivy.graphics import InstructionGroup

from logic.core.interfaces import IGameSystem
from kivy.core.image import Image as CoreImage

class EntitySystem(IGameSystem):



    def on_init(self):
        self.is_prey = True
        self.game.active_entities = []
        self.canvas_group = InstructionGroup()
        self.tex_cache = {}
        self.frame_counter = 0  # Счетчик для разделения нагрузки
        self.first_render = True  # Флаг, чтобы добавить группу ОДИН раз

    def on_update(self, dt):
        # 1. Берем текущие координаты головы змеи
        hx, hy = self.game.world_x, self.game.world_y

        # 2. Радиус укуса (увеличим до 50-55 пикселей для надежности) [15.1]
        eat_dist_sq = 55 ** 2

        # 3. Дистанция деспавна (чтобы не лагало)
        despawn_dist_sq = 2000 ** 2

        for ent in self.game.active_entities[:]:
            # Считаем вектор до змеи
            dx = ent.pos[0] - hx
            dy = ent.pos[1] - hy
            dist_sq = dx * dx + dy * dy

            # А. Удаляем далеких
            if dist_sq > despawn_dist_sq:
                self.game.active_entities.remove(ent)
                continue

            # Б. ПРОВЕРКА УКУСА (выполняем ДО обновления ИИ моба) [20.1]
            if dist_sq < eat_dist_sq:
                ent.on_catch()  # Начисляем очки и рост
                ent.alive = False
                self.game.active_entities.remove(ent)
                continue

            # В. Если не съели — обновляем ИИ (убегание)
            if ent.alive:
                ent.update(dt)

    def on_render(self, canvas, t, zoom):
        # 1. Очищаем только внутренности группы
        self.canvas_group.clear()

        # 2. Оптимизация: берем ссылки на методы заранее
        add_inst = self.canvas_group.add
        hx, hy = self.game.world_x, self.game.world_y

        for ent in self.game.active_entities:
            # 3. CULLING: Рисуем только тех, кто в радиусе видимости (1000px)
            dx = ent.pos[0] - hx
            dy = ent.pos[1] - hy
            if dx * dx + dy * dy < 1000000:
                ent.draw(self.canvas_group)  # Передаем группу

        # 4. ВАЖНО: Добавляем группу на холст только ОДИН раз за всю жизнь игры
        if self.first_render:
            canvas.add(self.canvas_group)
            self.first_render = False

    def get_tex(self, path):
        """
        Метод-помощник, который мобы вызывают в своем __init__.
        Гарантирует, что текстура грузится с диска только ОДИН раз. [15.1]
        """
        if path not in self.tex_cache:
            from kivy.core.image import Image as CoreImage
            try:
                tex = CoreImage(path).texture
                tex.mag_filter = 'nearest' # Для четкости
                self.tex_cache[path] = tex
            except Exception as e:
                print(f"Ошибка загрузки ассета {path}: {e}")
                return None
        return self.tex_cache[path]

    def spawn(self, entity_class, pos):
        """
        Универсальный спавн с защитой производительности 2025.
        """
        # 1. Жесткий лимит для стабильных 60 FPS на POCO X7 Pro
        if len(self.game.active_entities) >= 40:
            return None

        # 2. Создаем экземпляр моба
        new_ent = entity_class(self.game, pos)

        # 3. Добавляем в список активных сущностей
        self.game.active_entities.append(new_ent)

        return new_ent





    def _is_visible(self, ent):
        # Оптимизация: не считаем корень (sqrt), работаем с квадратами [12.1]
        dist_sq = (ent.pos[0] - self.game.world_x)**2 + (ent.pos[1] - self.game.world_y)**2
        return dist_sq < 1500**2  # Видимость в радиусе ~1500 пикселей

