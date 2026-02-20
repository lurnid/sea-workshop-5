# models/category.py (final)

from .project import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    projects = db.relationship('Project', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.id}: '{self.name}'>"
