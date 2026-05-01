from screens.base import BaseScreen


class ResourceDescScreen(BaseScreen):
    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        selected_name = self.app.state.settings.get("selected_resource_name")
        resource = None
        for item in self.app.state.resources:
            if item.get("name") == selected_name:
                resource = item
                break

        if resource is None:
            resource = self.app.state.resources[0] if self.app.state.resources else {
                "name": "Resource",
                "desc": "- description",
                "contact": "",
            }

        self.ids.resource_title.text = resource.get("name", "Resource")
        self.ids.resource_desc.text = resource.get("desc", "- description")
        self.ids.resource_contact.text = resource.get("contact", "")
