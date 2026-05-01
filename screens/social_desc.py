from screens.base import BaseScreen


class SocialDescScreen(BaseScreen):
    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        selected_id = self.app.state.settings.get("selected_event_id")
        event = None
        for e in self.app.state.events:
            if e.get("id") == selected_id:
                event = e
                break
        if not event:
            event = self.app.state.events[-1] if self.app.state.events else {"title": "Event", "description": "- description"}
        self.ids.event_title.text = event["title"]
        self.ids.event_desc.text = event["description"]
