# interface/menu_drawer.py
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDIconButton, MDRaisedButton, MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivymd.app import MDApp

from logic.core.config import MUTATIONS_CONFIG


class GameInterfaceManager:
    def setup_ui(self, screen):
        # 1. Кнопка меню
        self.menu_btn = MDIconButton(
            icon="menu",
            pos_hint={"top": 0.99, "x": 0.01},
            theme_text_color="Custom",
            text_color=(0, 1, 1, 1),
            on_release=self.toggle_menu
        )

        # 2. Мгновенная панель (на половину экрана)
        self.menu_panel = MDFloatLayout(
            size_hint=(0.5, 1.0),
            pos_hint={"x": -0.5, "y": 0},  # Изначально спрятана за левым краем
            md_bg_color=(0.1, 0.12, 0.1, 0.95),
            opacity=0
        )

        self.zoom_in_btn = MDIconButton(
            icon="magnify-plus",
            pos_hint={"right": 0.98, "center_y": 0.55},
            md_bg_color=(0, 0, 0, 0.3),
            on_release=lambda x: self.change_zoom(0.1)
        )

        self.zoom_out_btn = MDIconButton(
            icon="magnify-minus",
            pos_hint={"right": 0.98, "center_y": 0.45},
            md_bg_color=(0, 0, 0, 0.3),
            on_release=lambda x: self.change_zoom(-0.1)
        )

        # Метка мониторинга в ПРАВОМ верхнем углу
        self.fps_label = MDLabel(
            text="FPS: 0 | ENT: 0",
            # right: 0.98 прижимает к правому краю, top: 0.98 к верхнему
            pos_hint={"right": 0.98, "top": 0.98},
            size_hint=(None, None),
            size=(dp(200), dp(40)),
            halign="right",  # Текст выравниваем по правому краю
            theme_text_color="Custom",
            text_color=(0, 1, 0, 1),
            font_style="Caption",
            bold=True
        )
        screen.add_widget(self.fps_label)
        # Запускаем цикл обновления (раз в 0.5 сек)
        Clock.schedule_interval(self.update_debug_data, 0.5)

        screen.add_widget(self.zoom_in_btn)
        screen.add_widget(self.zoom_out_btn)


        # Статус для игры
        self.is_open = False

        screen.add_widget(self.menu_btn)
        screen.add_widget(self.menu_panel)



        # Автоматическое создание кнопок из конфига
        y_pos = 0.8
        for m_id, info in MUTATIONS_CONFIG.items():
            btn = MDFillRoundFlatButton(
                text=f"{info['name']}: {info['cost']} БИО",
                pos_hint={"center_x": 0.5, "center_y": y_pos},
                size_hint_x=0.8,
                md_bg_color=info['color'],
                on_release=lambda x, mid=m_id: self.buy_mutation(mid, x)
            )
            self.menu_panel.add_widget(btn)
            y_pos -= 0.12  # Смещаем следующую кнопку ниже

    def buy_mutation(self, m_id, instance):
        from kivymd.app import MDApp
        game = MDApp.get_running_app().game
        info = MUTATIONS_CONFIG[m_id]

        if game.biomass_points >= info['cost'] and not info['active']:
            game.biomass_points -= info['cost']
            info['active'] = True  # МЕНЯЕМ В КОНФИГЕ
            instance.text = f"{info['name']}: КУПЛЕНО"
            instance.disabled = True

    def toggle_menu(self, *args):
        if not self.is_open:
            # Мгновенно показать
            self.menu_panel.pos_hint = {"x": 0, "y": 0}
            self.menu_panel.opacity = 1
            self.is_open = True
        else:
            # Мгновенно скрыть
            self.menu_panel.pos_hint = {"x": -0.5, "y": 0}
            self.menu_panel.opacity = 0
            self.is_open = False

    def is_menu_open(self):
        return self.is_open

    def change_zoom(self, delta):
        from kivymd.app import MDApp
        game = MDApp.get_running_app().game

        # Плавное изменение с границами
        new_zoom = game.camera_zoom + delta
        # Ограничиваем зум от 0.3 (далеко) до 1.5 (близко)
        game.camera_zoom = max(0.3, min(1.5, new_zoom))
        print(f"Zoom changed to: {game.camera_zoom}")

    def update_debug_data(self, dt):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if not hasattr(app, 'game'): return

        game = app.game
        fps = Clock.get_fps()
        ent_count = len(getattr(game, 'active_entities', []))

        # АУДИТ УТЕЧКИ (Считаем инструкции на всех холстах) [15.1]
        # 1. Инструкции главного холста игры
        total_instr = len(game.canvas.children)

        # 2. Инструкции во всех системах (Snake, Entity, FX и др.)
        # Именно здесь в on_render скапливается мусор без canvas.clear() [12.1]
        if hasattr(game, 'manager'):
            for system in game.manager.systems:
                if hasattr(system, 'canvas'):
                    total_instr += len(system.canvas.children)

        # Выводим расширенную инфу
        self.fps_label.text = f"FPS: {int(fps)} | ENT: {ent_count} | INST: {total_instr}"

        # Визуальная диагностика [15.1]
        if fps < 45:
            self.fps_label.text_color = (1, 0, 0, 1)  # Красный - тормоза
        elif total_instr > 5000:
            self.fps_label.text_color = (1, 1, 0, 1)  # Желтый - риск утечки
        else:
            self.fps_label.text_color = (0, 1, 0, 1)  # Зеленый - ок

