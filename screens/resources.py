from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from screens.base import BaseScreen


class ResourcesScreen(BaseScreen):
    _filtered = []

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        if len(self.app.state.resources) < 6:
            extras = [
                {"name": "Career Center", "desc": "Resume and interview coaching.", "contact": "555-210-1100"},
                {"name": "Tutoring Lab", "desc": "Free math and science tutoring.", "contact": "555-220-3300"},
                {"name": "Library Help Desk", "desc": "Research and citation support.", "contact": "555-998-1200"},
                {"name": "IT Support", "desc": "Account and device troubleshooting.", "contact": "555-771-4411"},
            ]
            names = {r["name"] for r in self.app.state.resources}
            for resource in extras:
                if resource["name"] not in names:
                    self.app.state.resources.append(resource)
            self.app.persist()
        self.filter_resources(self.ids.search.text if "search" in self.ids else "")

    def filter_resources(self, query):
        q = (query or "").lower().strip()
        rows = [
            resource
            for resource in self.app.state.resources
            if q in resource["name"].lower()
            or q in resource["desc"].lower()
            or q in resource["contact"]
        ]
        self._filtered = rows

        box = self.ids.resource_list_box
        box.clear_widgets()

        if not rows:
            empty = Label(
                text="No resources found\nTry: counseling, writing, tutoring, IT",
                size_hint_y=None,
                height=120,
                color=(0, 0, 0, 1),
                bold=True,
                font_size="20sp",
                halign="center",
                valign="middle",
            )
            empty.bind(size=lambda label, *_: setattr(label, "text_size", label.size))
            box.add_widget(empty)
            return

        header = BoxLayout(size_hint_y=None, height=72)
        header.add_widget(Label(text="Resource", color=(0, 0, 0, 1), bold=True, font_size="22sp"))
        header.add_widget(Label(text="Contact info", color=(0, 0, 0, 1), bold=True, font_size="22sp"))
        box.add_widget(header)

        for index, resource in enumerate(rows):
            row = BoxLayout(size_hint_y=None, height=104, padding=[4, 6, 4, 6], spacing=8)
            details = Label(
                text=f"{resource['name']}\n- {resource['desc']}",
                color=self.app.text_color,
                bold=True,
                font_size=self.app.sp(17),
                halign="left",
                valign="middle",
            )
            details.bind(size=lambda label, *_: setattr(label, "text_size", label.size))
            row.add_widget(details)

            contact = Label(
                text=resource["contact"],
                color=self.app.text_color,
                bold=True,
                font_size=self.app.sp(17),
                size_hint_x=.42,
                halign="left",
                valign="middle",
            )
            contact.bind(size=lambda label, *_: setattr(label, "text_size", label.size))
            row.add_widget(contact)

            arrow = Button(
                text=">",
                size_hint_x=None,
                width=42,
                background_normal="",
                background_color=(0, 0, 0, 0),
                color=self.app.text_color,
                bold=True,
                font_size=self.app.sp(26),
            )
            arrow.bind(on_release=lambda _, i=index: self.open_desc(i))
            row.add_widget(arrow)
            box.add_widget(row)

    def open_desc(self, filtered_index):
        if filtered_index < len(self._filtered):
            selected = self._filtered[filtered_index]
            self.app.state.settings["selected_resource_name"] = selected["name"]
            self.app.persist()
        self.go("resource_desc")
