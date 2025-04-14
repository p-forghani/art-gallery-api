from backend.app import create_app, db
from backend.app.models.user import Role


def initialize_roles():
    """
    Initialize default roles in the database with hardcoded IDs.
    """
    roles = [
        {"id": 1, "name": "admin"},
        {"id": 2, "name": "artist"},
        {"id": 3, "name": "user"}
    ]
    app = create_app()

    with app.app_context():
        for role in roles:
            # Check if the role already exists
            existing_role = Role.query.filter_by(id=role["id"]).first()
            if not existing_role:
                # Create the role if it doesn't exist
                new_role = Role(id=role["id"], name=role["name"])
                db.session.add(new_role)
                print(f"Added role: {role['name']} with ID {role['id']}")
            else:
                print(f"Role already exists: {role['name']} with ID {role['id']}")
        db.session.commit()
        print("Roles initialized successfully.")