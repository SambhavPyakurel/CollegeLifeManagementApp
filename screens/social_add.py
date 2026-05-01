from datetime import date
from screens.base import BaseScreen


class SocialAddScreen(BaseScreen):
    def confirm(self):
        title = self.ids.event_title.text.strip() or "Event"
        desc = self.ids.event_desc.text.strip() or "Description"
        category = "sports" if self.ids.cat_sports.active else "academic" if self.ids.cat_academic.active else "stud_life" if self.ids.cat_life.active else "stud_life"
        next_id = max([e["id"] for e in self.app.state.events], default=0) + 1
        self.app.state.events.append({
            "id": next_id,
            "title": title,
            "description": desc,
            "date": str(date.today()),
            "category": category,
        })
        self.app.persist()
        self.go("social")

    def cancel(self):
        self.go("social")
