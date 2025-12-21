# interface/menu_drawer.py
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.core.window import Window


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

        # Контент
        self.title_label = MDLabel(
            text="МУТАЦИИ",
            halign="center",
            pos_hint={"top": 0.95},
            theme_text_color="Custom",
            text_color=(0, 1, 1, 1),
            font_style="H6"
        )
        self.mutation_btn = MDRaisedButton(
            text="Мутация: Хищный выпад (5 биомассы)",
            pos_hint={"center_x": 0.5, "center_y": 0.8},
            md_bg_color=(0, 0.5, 0.5, 1),
            on_release=self.buy_snap_mutation
        )
        self.menu_panel.add_widget(self.mutation_btn)

        self.menu_panel.add_widget(self.title_label)

        # Статус для игры
        self.is_open = False

        screen.add_widget(self.menu_btn)
        screen.add_widget(self.menu_panel)

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

    def buy_snap_mutation(self, instance):
        from kivymd.app import MDApp
        game = MDApp.get_running_app().game

        # Проверяем, хватает ли очков биомассы
        if game.biomass_points >= 5 and not game.mutations["predatory_snap"]:
            game.biomass_points -= 5
            game.mutations["predatory_snap"] = True
            instance.text = "Мутация: КУПЛЕНО"
            instance.disabled = True
