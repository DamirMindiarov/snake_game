class SystemManager:
    def __init__(self, game):
        self.game = game
        self.systems = []

    def register(self, system_instance):
        system_instance.on_init()
        self.systems.append(system_instance)
        return system_instance

    def update_all(self, dt):
        for s in self.systems:
            s.on_update(dt)

    def render_all(self, canvas, t, zoom):
        for s in self.systems:
            s.on_render(canvas, t, zoom)

    def broadcast_chunk(self, cx, cy, chunk_data):
        for s in self.systems:
            s.on_chunk_generated(cx, cy, chunk_data)
