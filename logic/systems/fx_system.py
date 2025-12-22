# logic/systems/fx_system.py
from logic.core.interfaces import IGameSystem

class FXSystem(IGameSystem):
    def on_init(self):
        self.active_effects = []

    def spawn(self, effect_instance):
        """Метод для внешнего вызова: добавить эффект в очередь"""
        self.active_effects.append(effect_instance)

    def on_update(self, dt):
        for e in self.active_effects[:]:
            e.update(dt)
            if not e.is_alive:
                self.active_effects.remove(e)

    def on_render(self, canvas, t, zoom):
        for e in self.active_effects:
            e.draw(canvas)
