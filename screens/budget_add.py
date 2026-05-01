from screens.base import BaseScreen

class BudgetAddScreen(BaseScreen):
    def confirm(self):
        category = self.ids.category_input.text.strip() or "Category 1"
        try:
            amount = float(self.ids.amount_input.text.strip() or "0")
        except ValueError:
            amount = 0.0
        next_id = max([t["id"] for t in self.app.state.transactions], default=0) + 1
        self.app.state.transactions.append({"id": next_id, "category": category, "amount": amount})
        self.app.persist()
        self.go("budget")

    def delete_last(self):
        if self.app.state.transactions:
            self.app.state.transactions.pop()
            self.app.persist()
        self.go("budget")

    def cancel(self):
        self.go("budget")

