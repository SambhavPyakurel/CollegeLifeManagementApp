from collections import defaultdict
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from screens.base import BaseScreen


class BudgetScreen(BaseScreen):
    PIE_COLORS = [
        [1.00, 0.22, 0.24, 1],
        [0.00, 0.53, 1.00, 1],
        [0.95, 0.76, 0.00, 1],
        [0.20, 0.78, 0.35, 1],
    ]

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.refresh_budget()

    def refresh_budget(self):
        spent = sum(float(t.get("amount", 0)) for t in self.app.state.transactions)
        income = 120.00
        remaining = self.app.state.budget_limit - spent

        self.ids.current_balance.text = f"${remaining:.2f}"
        self.ids.total_income.text = f"${income:.2f}"
        self.ids.total_expenses.text = f"${spent:.2f}"
        self.ids.weekly_spent.text = f"${spent:.2f}/${self.app.state.budget_limit:.0f}"
        self.ids.remaining_text.text = f"${max(remaining, 0):.2f} remaining"
        self.ids.limit_text.text = f"${self.app.state.budget_limit:.0f}"

        ratio = 0 if self.app.state.budget_limit <= 0 else min(1, spent / self.app.state.budget_limit)
        self.ids.progress.value = ratio * 100

        by_cat = defaultdict(float)
        for t in self.app.state.transactions:
            by_cat[t.get("category", "Other")] += float(t.get("amount", 0))

        sorted_items = sorted(by_cat.items(), key=lambda x: x[1], reverse=True)
        top3 = sorted_items[:3]
        others_total = sum(v for _, v in sorted_items[3:])

        labels = [k for k, _ in top3]
        values = [v for _, v in top3]
        if others_total > 0:
            labels.append("Others")
            values.append(others_total)

        if not values:
            labels = ["Category 1", "Category 2", "Category 3", "Others"]
            values = [1, 1, 1, 1]

        self.ids.pie.values = values
        self.ids.pie.colors = self.PIE_COLORS[:len(values)]

        dot_sources = ["assets/red.png", "assets/blue.png", "assets/yellow.png", "assets/green.png"]
        label_ids = [self.ids.ltxt1, self.ids.ltxt2, self.ids.ltxt3, self.ids.ltxt4]
        dot_ids = [self.ids.ldot1, self.ids.ldot2, self.ids.ldot3, self.ids.ldot4]

        for i in range(4):
            if i < len(labels):
                label_ids[i].text = labels[i]
                dot_ids[i].source = dot_sources[i]
                label_ids[i].opacity = 1
                dot_ids[i].opacity = 1
            else:
                label_ids[i].text = ""
                dot_ids[i].source = ""
                label_ids[i].opacity = 0
                dot_ids[i].opacity = 0

        self._render_transactions()

    def _render_transactions(self):
        box = self.ids.txn_list
        box.clear_widgets()
        if not self.app.state.transactions:
            box.add_widget(Label(
                text="No transactions yet",
                size_hint_y=None,
                height=36,
                color=self.app.muted_text_color,
                font_size="14sp",
            ))
            return

        for tx in reversed(self.app.state.transactions[-5:]):
            row = BoxLayout(size_hint_y=None, height=38, spacing=8)
            row.add_widget(Label(
                text=f"#{tx['id']} {tx['category']}: ${float(tx['amount']):.2f}",
                color=self.app.text_color,
                halign="left",
                valign="middle",
            ))
            delete = Button(
                text="Delete",
                size_hint_x=None,
                width=86,
                background_normal="",
                background_color=(0.85, 0.15, 0.15, 1),
                color=(1, 1, 1, 1),
            )
            delete.bind(on_release=lambda _, tx_id=tx["id"]: self.delete_transaction(tx_id))
            row.add_widget(delete)
            box.add_widget(row)

    def delete_transaction(self, tx_id):
        self.app.state.transactions = [
            tx for tx in self.app.state.transactions if tx.get("id") != tx_id
        ]
        self.app.persist()
        self.refresh_budget()

    def open_add(self):
        self.go("budget_add")

    def open_set_limit(self):
        root = BoxLayout(orientation="vertical", padding=12, spacing=8)
        field = TextInput(text=str(int(self.app.state.budget_limit)), multiline=False, input_filter="float")
        actions = BoxLayout(size_hint_y=None, height=44, spacing=8)
        ok = Button(text="Save")
        cancel = Button(text="Cancel")
        actions.add_widget(ok)
        actions.add_widget(cancel)
        root.add_widget(Label(text="Set Budget Limit"))
        root.add_widget(field)
        root.add_widget(actions)
        pop = Popup(title="Budget Limit", content=root, size_hint=(0.65, 0.35))

        def save(*_):
            try:
                self.app.state.budget_limit = max(1.0, float(field.text.strip() or "750"))
            except ValueError:
                self.app.state.budget_limit = 750.0
            self.app.persist()
            self.refresh_budget()
            pop.dismiss()

        ok.bind(on_release=save)
        cancel.bind(on_release=lambda *_: pop.dismiss())
        pop.open()
