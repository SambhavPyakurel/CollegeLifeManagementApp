from kivy.app import App
from kivy.graphics import Color, Ellipse
from kivy.properties import ListProperty
from kivy.uix.widget import Widget


class PieWidget(Widget):
    values = ListProperty([40, 35, 25])
    colors = ListProperty([
        [0.20, 0.78, 0.35, 1],
        [0.00, 0.53, 1.00, 1],
        [1.00, 0.22, 0.24, 1],
    ])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._redraw, size=self._redraw, values=self._redraw, colors=self._redraw)

    def _redraw(self, *args):
        self.canvas.clear()
        total = float(sum(v for v in self.values if v > 0))
        if total <= 0:
            total = 1.0
            vals = [1]
            cols = [[0.85, 0.85, 0.85, 1]]
        else:
            vals = self.values
            cols = self.colors

        with self.canvas:
            start = 0
            for i, val in enumerate(vals):
                if val <= 0:
                    continue
                sweep = (val / total) * 360.0
                Color(*cols[i % len(cols)])
                Ellipse(pos=self.pos, size=self.size, angle_start=start, angle_end=start + sweep)
                start += sweep

            hole_w = self.size[0] * 0.55
            hole_h = self.size[1] * 0.55
            hx = self.pos[0] + (self.size[0] - hole_w) / 2
            hy = self.pos[1] + (self.size[1] - hole_h) / 2
            app = App.get_running_app()
            Color(*(app.card_color if app else [0.97, 0.97, 0.97, 1]))
            Ellipse(pos=(hx, hy), size=(hole_w, hole_h))
