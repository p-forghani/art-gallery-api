from src.app.models import Role


def initialize_roles(app, db):
    """
    Initialize default roles in the database with hardcoded IDs.
    """
    roles = [
        {"id": 1, "name": "admin"},
        {"id": 2, "name": "artist"},
        {"id": 3, "name": "user"}
    ]

    with app.app_context():
        for role in roles:
            # Check if the role already exists
            existing_role = Role.query.filter_by(id=role["id"]).first()
            if not existing_role:
                # Create the role if it doesn't exist
                new_role = Role(id=role["id"], name=role["name"])
                db.session.add(new_role)
        db.session.commit()
        print("Roles initialized successfully.")
