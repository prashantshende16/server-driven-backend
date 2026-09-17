from sqlalchemy.future import select
from app.core.database import AsyncSessionLocal
from app.models import Page, Form, ModelDefinition, Navigation, AppConfig

async def seed_initial_data():
    async with AsyncSessionLocal() as session:
        # Check if pages exist
        result = await session.execute(select(Page).limit(1))
        if result.scalar_one_or_none():
            return  # Already seeded

        # 1. Seed Home Page
        home_page = Page(
            name="Home",
            slug="home",
            title="Home",
            description="Default server-driven landing page",
            route="/home",
            layout_type="scroll",
            status="published",
            is_published=True,
            components=[
                {
                    "id": "banner_1",
                    "type": "banner",
                    "order": 1,
                    "props": {
                        "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800",
                        "title": "Welcome to FlowForge",
                        "subtitle": "Server-driven dynamic mobile applications"
                    }
                },
                {
                    "id": "heading_1",
                    "type": "heading",
                    "order": 2,
                    "props": {
                        "text": "Upcoming Highlights"
                    }
                },
                {
                    "id": "events_1",
                    "type": "list",
                    "order": 3,
                    "data_source": {
                        "type": "api",
                        "endpoint": "/api/v1/events"
                    }
                }
            ]
        )
        session.add(home_page)

        # 2. Seed Event Model Definition
        event_model = ModelDefinition(
            name="event",
            slug="events",
            label="Event",
            description="Manage conferences and community events",
            is_published=True,
            fields=[
                {"name": "title", "label": "Title", "type": "text", "required": True},
                {"name": "description", "label": "Description", "type": "textarea"},
                {"name": "image", "label": "Image", "type": "image"},
                {"name": "event_date", "label": "Event Date", "type": "datetime"}
            ]
        )
        session.add(event_model)

        # 3. Seed Registration Form
        member_form = Form(
            name="member_registration",
            slug="member_registration",
            title="Member Registration",
            description="Sign up for FlowForge membership",
            is_published=True,
            fields=[
                {"name": "first_name", "label": "First Name", "type": "text", "required": True, "placeholder": "Jane"},
                {"name": "email", "label": "Email Address", "type": "email", "required": True, "placeholder": "jane@example.com"}
            ],
            submit_action={
                "method": "POST",
                "endpoint": "/api/v1/members"
            },
            success_message="Thank you for registering!",
            failure_message="Could not complete registration."
        )
        session.add(member_form)

        # 4. Seed Navigation Tabs
        bottom_nav = Navigation(
            name="Main Bottom Tabs",
            slug="main_bottom_tabs",
            nav_type="bottom_tabs",
            is_active=True,
            items=[
                {"title": "Home", "icon": "home", "page": "home"},
                {"title": "Events", "icon": "calendar", "page": "events"},
                {"title": "Profile", "icon": "user", "page": "profile"}
            ]
        )
        session.add(bottom_nav)

        # 5. App Config
        app_config = AppConfig(
            schema_version={"version": 1, "app_name": "FlowForge", "min_version": "1.0.0"},
            theme={"primary_color": "#2563eb", "dark_mode": False},
            navigation={"type": "bottom_tabs"}
        )
        session.add(app_config)

        await session.commit()
