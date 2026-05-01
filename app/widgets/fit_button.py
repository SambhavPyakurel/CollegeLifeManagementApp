from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.button import Button


class AutoFitButton(Button):
    min_font_size = NumericProperty(9)
    horizontal_padding = NumericProperty(10)
    vertical_padding = NumericProperty(6)

    def __init__(self, **kwargs):
        self._fitting = False
        self._preferred_font_size = 0
        super().__init__(**kwargs)
        self.bind(
            size=self._schedule_fit,
            text=self._schedule_fit,
            texture_size=self._schedule_fit,
        )
        self.bind(font_size=self._remember_preferred)

    def on_kv_post(self, base_widget):
        self.halign = "center"
        self.valign = "middle"
        self.shorten = False
        self._remember_preferred()
        self._schedule_fit()

    def _remember_preferred(self, *_):
        if self._fitting:
            return
        self._preferred_font_size = float(self.font_size)
        self._schedule_fit()

    def _schedule_fit(self, *_):
        Clock.unschedule(self._fit_text)
        Clock.schedule_once(self._fit_text, 0)

    def _fit_text(self, *_):
        if self._fitting or self.width <= 0 or self.height <= 0:
            return

        self._fitting = True
        try:
            available_width = max(1, self.width - (self.horizontal_padding * 2))
            available_height = max(1, self.height - (self.vertical_padding * 2))
            self.text_size = (None, None)
            self.font_size = self._preferred_font_size or float(self.font_size)
            self.texture_update()

            while float(self.font_size) > self.min_font_size and (
                self.texture_size[0] > available_width
                or self.texture_size[1] > available_height
            ):
                self.font_size = max(self.min_font_size, float(self.font_size) - 1)
                self.texture_update()
        finally:
            self._fitting = False
