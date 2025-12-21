# logic/collisions.py

# logic/collisions.py

class CollisionMixin:
    def check_movement_with_collisions(self, vx, vy):
        """Проверяет возможность сдвига и реализует скольжение вдоль стен"""

        # 1. Пробуем сдвинуться по X
        future_x = self.world_x + vx
        if not self.is_tile_solid(future_x, self.world_y):
            self.world_x = future_x
        else:
            # Если по X стена — гасим скорость по X и красим голову
            self.vel_x = 0
            self.damage_timer = 0.5

            # 2. Пробуем сдвинуться по Y (независимо от X)
        future_y = self.world_y + vy
        if not self.is_tile_solid(self.world_x, future_y):
            self.world_y = future_y
        else:
            # Если по Y стена — гасим скорость по Y и красим голову
            self.vel_y = 0
            self.damage_timer = 0.5

    def handle_obstacle_hit(self, tx, ty, cx, cy):
        # Если у змеи есть мутация 'crusher'
        if getattr(self, 'has_crusher_mutation', False):
            # Удаляем камень из данных
            self.obstacles[(cx, cy)]["stones"].remove((tx, ty))
            # Перерисовываем чанк
            self.redraw_chunk(cx, cy)
        else:
            # Иначе — обычное столкновение и урон
            self.damage_timer = 0.5
            self.vel_x *= -0.5
            self.vel_y *= -0.5