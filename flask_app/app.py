# app.py (final — with full CRUD functionality)

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, redirect, url_for, abort
from models import db, Project, Category

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# =============================================================================
# READ ROUTES
# =============================================================================

@app.route('/')
def index():
    """Display all projects."""
    projects = Project.query.all()
    return render_template('index.html', projects=projects)


@app.route('/about')
def about():
    """Display the about page (static route)."""
    return render_template('about.html')


@app.route('/projects/<int:id>')
def project_detail(id):
    """Display a single project by ID."""
    project = db.session.get(Project, id)
    if project is None:
        abort(404)
    return render_template('project_detail.html', project=project)


@app.route('/categories/<int:id>')
def category_detail(id):
    """Display all projects in a category."""
    category = db.session.get(Category, id)
    if category is None:
        abort(404)
    return render_template('category_detail.html', category=category)


# =============================================================================
# CREATE ROUTE
# =============================================================================

@app.route('/add', methods=['GET', 'POST'])
def add_project():
    """Add a new project."""
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        category_id = request.form.get('category_id')

        # Convert empty string to None for category_id
        if category_id == '' or category_id is None:
            category_id = None
        else:
            category_id = int(category_id)

        new_project = Project(name=name, description=description, category_id=category_id)
        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for('index'))

    # GET request — show the form with categories for dropdown
    categories = Category.query.all()
    return render_template('add_project.html', categories=categories)


# =============================================================================
# UPDATE ROUTE
# =============================================================================

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    """Edit an existing project."""
    project = db.session.get(Project, id)

    if project is None:
        abort(404)

    if request.method == 'POST':
        project.name = request.form['name']
        project.description = request.form.get('description', '')
        category_id = request.form.get('category_id')

        # Convert empty string to None for category_id
        if category_id == '' or category_id is None:
            project.category_id = None
        else:
            project.category_id = int(category_id)

        db.session.commit()
        return redirect(url_for('index'))

    # GET request — show the form with categories for dropdown
    categories = Category.query.all()
    return render_template('edit_project.html', project=project, categories=categories)


# =============================================================================
# DELETE ROUTE
# =============================================================================

@app.route('/delete/<int:id>')
def delete_project(id):
    """Delete a project."""
    project = db.session.get(Project, id)

    if project is None:
        abort(404)

    db.session.delete(project)
    db.session.commit()

    return redirect(url_for('index'))


# =============================================================================
# RUN THE APPLICATION
# =============================================================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
