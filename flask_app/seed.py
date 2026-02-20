# seed.py

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, Category

with app.app_context():
    # Create tables (adds new Category table, preserves existing data)
    db.create_all()
    print("Database schema updated.")

    # Check if categories already exist
    if Category.query.first():
        print("\nCategories already exist — skipping seed.")
    else:
        # Create categories
        categories = [
            Category(name="Web Apps"),
            Category(name="Data Science"),
            Category(name="Automation"),
        ]
        db.session.add_all(categories)
        db.session.commit()

        print("\nCategories created:")
        for cat in categories:
            print(f"   [{cat.id}] {cat.name}")

    print("\nDone!")
