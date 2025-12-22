import random
import math
from kivy.graphics import Color, Ellipse
from logic.core.interfaces import IGameSystem

class FXSystem(IGameSystem):
    def __init__(self, game):
        super().__init__(game)
        # Инициализируем атрибуты СРАЗУ при создании объекта
        self.active_effects = []   # Для GhostTrail (шлейф мутации)
        self.bite_particles = []   # Для батчинга частиц (укусы)
        self.enabled = True        # По умолчанию включено

    def on_init(self):
        # Синхронизируем настройки из игры, если они есть
        self.enabled = getattr(self.game, 'fx_bite_enabled', True)

    def spawn(self, effect_instance):
        """Для тяжелых эффектов (шлейф рывка)"""
        self.active_effects.append(effect_instance)

    def spawn_bite(self, x=0, y=0):
        """Батчинг частиц для укусов [20.1]"""
        if not self.enabled:
            return
        for _ in range(18):
            angle = random.uniform(0, 6.28)
            speed = random.uniform(4, 12)
            self.bite_particles.append({
                'lx': 0.0, 'ly': 0.0, # Локальное смещение
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': 1.0,
                's': random.uniform(6, 12)
            })

    def on_update(self, dt):
        # 1. Обновляем шлейфы
        for e in self.active_effects[:]:
            e.update(dt)
            if not e.is_alive:
                self.active_effects.remove(e)

        # 2. Обновляем частицы укуса (используем копию списка для безопасности)
        for p in self.bite_particles[:]:
            p['lx'] += p['vx']
            p['ly'] += p['vy']
            p['vx'] *= 0.92
            p['vy'] *= 0.92
            p['life'] -= dt * 2.0
            if p['life'] <= 0:
                self.bite_particles.remove(p)

    def on_render(self, canvas, t, zoom):
        # Берем координаты головы в момент отрисовки для идеальной привязки [15.1]
        hx, hy = self.game.world_x, self.game.world_y

        # Рисуем частицы батчем
        if self.bite_particles:
            for p in self.bite_particles:
                canvas.add(Color(0.7, 0.7, 0.7, p['life']))
                canvas.add(Ellipse(
                    pos=(hx + p['lx'] - p['s']/2, hy + p['ly'] - p['s']/2),
                    size=(p['s'], p['s'])
                ))

        # Рисуем объектные эффекты
        for e in self.active_effects:
            if e.is_alive:
                e.draw(canvas)
