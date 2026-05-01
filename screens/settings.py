from screens.base import BaseScreen

class SettingsScreen(BaseScreen):
    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        s = self.app.state.settings
        self.ids.dark_mode.active = bool(s.get("dark_mode", False))
        scale = float(s.get("font_scale", 1.0))
        self.ids.font_size.value = max(1, min(10, int(round((scale - 0.80) / 0.05))))
        self.ids.font_val.text = str(int(self.ids.font_size.value))

    def save_settings(self):
        self.app.state.settings["dark_mode"] = self.ids.dark_mode.active
        self.app.state.settings["font_scale"] = round(0.80 + (float(self.ids.font_size.value) * 0.05), 2)
        self.ids.font_val.text = str(int(self.ids.font_size.value))
        self.app.persist()
        self.app.apply_settings_theme()
        self._apply_theme_colors(self)

    def reset_app(self):
        self.app.store.reset()
        self.app.state = self.app.store.load()
        self.app.apply_settings_theme()
        self.on_pre_enter()
