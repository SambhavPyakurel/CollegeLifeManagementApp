from kivy.app import App
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from app.widgets import AutoFitButton, NavIconButton, PieWidget  # noqa: F401

from services.storage import StorageService
from screens.dashboard import DashboardScreen
from screens.routine import RoutineScreen
from screens.routine_add import RoutineAddScreen
from screens.budget import BudgetScreen
from screens.budget_add import BudgetAddScreen
from screens.resources import ResourcesScreen
from screens.resource_desc import ResourceDescScreen
from screens.social import SocialScreen
from screens.social_add import SocialAddScreen
from screens.social_desc import SocialDescScreen
from screens.settings import SettingsScreen


class CollegeLifeApp(App):
    bg_color = ListProperty([0.90, 0.95, 0.94, 1])
    header_color = ListProperty([0.50, 0.73, 0.73, 1])
    card_color = ListProperty([0.97, 0.97, 0.97, 1])
    nav_color = ListProperty([0.20, 0.20, 0.20, 1])
    text_color = ListProperty([0.05, 0.05, 0.05, 1])
    muted_text_color = ListProperty([0.84, 0.84, 0.84, 1])
    font_scale = NumericProperty(1.0)
    layout_scale = NumericProperty(1.0)

    def build(self):
        self.title = "College Life App"
        self.store = StorageService()
        self.state = self.store.load()
        Window.bind(size=lambda *_: self.update_layout_scale())
        self.update_layout_scale()
        self.apply_settings_theme()

        Factory.register("DashboardScreen", cls=DashboardScreen)
        Factory.register("RoutineScreen", cls=RoutineScreen)
        Factory.register("RoutineAddScreen", cls=RoutineAddScreen)
        Factory.register("BudgetScreen", cls=BudgetScreen)
        Factory.register("BudgetAddScreen", cls=BudgetAddScreen)
        Factory.register("ResourcesScreen", cls=ResourcesScreen)
        Factory.register("ResourceDescScreen", cls=ResourceDescScreen)
        Factory.register("SocialScreen", cls=SocialScreen)
        Factory.register("SocialAddScreen", cls=SocialAddScreen)
        Factory.register("SocialDescScreen", cls=SocialDescScreen)
        Factory.register("SettingsScreen", cls=SettingsScreen)
        Factory.register("NavIconButton", cls=NavIconButton)
        Factory.register("AutoFitButton", cls=AutoFitButton)

        for kv in [
            "kv/dashboard.kv",
            "kv/routine.kv",
            "kv/routine_add.kv",
            "kv/budget.kv",
            "kv/budget_add.kv",
            "kv/resources.kv",
            "kv/resource_desc.kv",
            "kv/social.kv",
            "kv/social_add.kv",
            "kv/social_desc.kv",
            "kv/settings.kv",
        ]:
            Builder.load_file(kv)

        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(RoutineScreen(name="routine"))
        sm.add_widget(RoutineAddScreen(name="routine_add"))
        sm.add_widget(BudgetScreen(name="budget"))
        sm.add_widget(BudgetAddScreen(name="budget_add"))
        sm.add_widget(ResourcesScreen(name="resources"))
        sm.add_widget(ResourceDescScreen(name="resource_desc"))
        sm.add_widget(SocialScreen(name="social"))
        sm.add_widget(SocialAddScreen(name="social_add"))
        sm.add_widget(SocialDescScreen(name="social_desc"))
        sm.add_widget(SettingsScreen(name="settings"))
        return sm

    def persist(self):
        self.store.save(self.state)

    def sp(self, base):
        return f"{max(9, base * float(self.font_scale) * float(self.layout_scale))}sp"

    def update_layout_scale(self):
        width_scale = Window.width / 412.0 if Window.width else 1.0
        height_scale = Window.height / 780.0 if Window.height else 1.0
        self.layout_scale = max(0.68, min(1.0, width_scale, height_scale))
        current = getattr(getattr(self, "root", None), "current_screen", None)
        if current and hasattr(current, "_apply_font_scale"):
            current._apply_font_scale(current)

    def apply_settings_theme(self):
        s = self.state.settings
        self.font_scale = float(s.get("font_scale", 1.0))
        dark = bool(s.get("dark_mode", False))
        if dark:
            self.bg_color = [0.08, 0.12, 0.13, 1]
            self.header_color = [0.31, 0.55, 0.55, 1]
            self.card_color = [0.14, 0.19, 0.20, 1]
            self.nav_color = [0.07, 0.09, 0.10, 1]
            self.text_color = [0.94, 0.97, 0.97, 1]
            self.muted_text_color = [0.60, 0.66, 0.66, 1]
        else:
            self.bg_color = [0.90, 0.95, 0.94, 1]
            self.header_color = [0.50, 0.73, 0.73, 1]
            self.card_color = [0.97, 0.97, 0.97, 1]
            self.nav_color = [0.20, 0.20, 0.20, 1]
            self.text_color = [0.05, 0.05, 0.05, 1]
            self.muted_text_color = [0.84, 0.84, 0.84, 1]
        Window.clearcolor = self.bg_color


if __name__ == "__main__":
    CollegeLifeApp().run()
