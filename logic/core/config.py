# logic/core/config.py

GAME_CONFIG = {
    "tile_size": 60,
    "chunk_size": 20,
    "snake_max_v": 9.0,
    "snake_accel": 0.4
}

MUTATIONS_CONFIG = {
    "predatory_snap": {
        "name": "ХИЩНЫЙ ВЫПАД",
        "cost": 5,
        "color": (0, 0.5, 0.5, 1),
        "active": True
    },
    "dash": {
        "name": "РЫВОК",
        "cost": 10,
        "color": (0.5, 0.2, 0.5, 1),
        "active": True
    }
}
