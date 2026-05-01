from dataclasses import dataclass, field
from datetime import date, timedelta
from random import choice


EVENT_CATEGORIES = ["stud_life", "academic", "sports"]


@dataclass
class AppState:
    settings: dict = field(default_factory=lambda: {
        "dark_mode": False,
        "font_scale": 1.0,
        "theme": "teal",
    })
    tasks: list = field(default_factory=list)
    transactions: list = field(default_factory=list)
    budget_limit: float = 750.0
    resources: list = field(default_factory=lambda: [
        {"name": "Counseling Services", "desc": "Mental health support.", "contact": "123-456-7890"},
        {"name": "Writing Center", "desc": "Essay and writing help.", "contact": "012-465-9837"},
    ])
    events: list = field(default_factory=lambda: [
        {"id": 1, "title": "Event 1", "description": "Campus mixer", "date": str(date.today()), "category": choice(EVENT_CATEGORIES)},
        {"id": 2, "title": "Event 2", "description": "Study jam", "date": str(date.today() + timedelta(days=1)), "category": choice(EVENT_CATEGORIES)},
        {"id": 3, "title": "Event 3", "description": "Club fair", "date": str(date.today() + timedelta(days=2)), "category": choice(EVENT_CATEGORIES)},
    ])
