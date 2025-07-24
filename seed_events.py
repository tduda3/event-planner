from datetime import datetime, timedelta

from app import create_app
from app.models import User
from app.services.user_service import UserService
from app.services.event_service import EventService

app = create_app()

SAMPLE_EVENTS = [
    ("Python Meetup", "Community Center", "Weekly Python enthusiast meetup"),
    ("Startup Pitch Night", "Innovation Hub", "Local startups pitch to investors"),
    ("Art Exhibition", "City Gallery", "Opening night of modern art show"),
    ("Pilates in the Park", "Riverside Park", "Outdoor pilates session for all levels"),
    ("Jazz Concert", "Downtown Club", "Evening of live jazz music"),
    ("Tech Careers Fair", "Convention Center", "Meet tech companies hiring"),
    ("Cooking Workshop", "Culinary School", "Hands-on Italian cooking class"),
    ("Book Club", "Library", "Discuss this month's novel"),
    ("Wine Tasting", "Vineyard Estate", "Sample local wines"),
    ("Board Game Night", "Cafe 123", "Bring your favorite board games"),
]

with app.app_context():
    user = User.query.filter_by(email="demo@example.com").first()
    if not user:
        user = UserService.create_user("demo", "demo@example.com", "password123")
    if not user.events:
        now = datetime.utcnow()
        for i, (title, location, desc) in enumerate(SAMPLE_EVENTS):
            dt = (now + timedelta(days=i + 1)).replace(microsecond=0)
            EventService.create_event(
                user.id,
                {
                    "title": title,
                    "datetime": dt.isoformat(),
                    "location": location,
                    "description": desc,
                },
            )
        print("Seeded sample events.")
    else:
        print("Demo events already exist.")

