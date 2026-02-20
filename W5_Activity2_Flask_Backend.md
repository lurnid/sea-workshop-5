# Workshop 5: Activity 2: Build a Flask Back-End

## What we're building

In this activity, we'll take the Flask application you built in Workshop 4 and:
1. **Refactor it** into a proper MVC (Model-View-Controller) structure
2. **Add new routes** for viewing individual projects and an About page
3. **Introduce a second table** (Categories) that relates to Projects

| Part | What we'll do | Estimated time |
|------|---------------|----------------|
| Prerequisites | Verify your W4 app is running, back it up | ~5 min |
| 1 | Refactor into MVC folders | ~10 min |
| 2 | Add static and dynamic routes | ~20 min |
| 3 | Create a Category model with relationships | ~30 min |
| 4 | Update templates to show categories | ~15 min |
| 5 | Practice exercises | ~10 min |

---

### This is a refactoring exercise

Unlike Workshop 4 where we built from scratch, today we're **reorganising existing code**. This is a common real-world task. As applications grow, you need to restructure them for maintainability.

You'll be:
- **Creating new files** in organised folders
- **Cutting** code from your existing `app.py`
- **Pasting** it into the new files
- **Updating imports** so everything still connects

This prepares you for your end-of-module assessment, where you'll need to build a non-trivial application with multiple related models and proper structure.

---

## Prerequisites: Verify and Back Up Your Workshop 4 Application

Before we begin, make sure your Workshop 4 Flask application is working correctly.

### Step 1: Verify it works

1. Open your W4 project folder in VS Code
2. Run the application: `python app.py`
3. Open http://127.0.0.1:5000 in your browser
4. Confirm you can:
   - See the project list (even if empty)
   - Click "Add New Project" and create a project
   - Edit and delete projects
5. Stop the server (Ctrl+C)


### Step 2: Back up your code

Before we start refactoring, **make a copy of your entire project folder**. This is your safety net.

```bash
# In your terminal, from the parent directory of your project:
cp -r flask_project flask_project_backup
```

Or simply copy the folder in your file explorer.

**Once backed up, let your tutor know you're ready.**

### Your W4 Starting Point

Your Workshop 4 `app.py` should look like this (a complete CRUD application with routes):

```python
# ============================================================
# STARTING POINT: Your W4 app.py (before refactoring)
# ============================================================

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# --- Create the Flask application ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# --- Define the Project model ---
class Project(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<Project {self.id}: {self.name}>'


# --- READ: List all projects ---
@app.route('/')
def list_projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)


# --- CREATE: Add a new project ---
@app.route('/add', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')

        new_project = Project(name=name, description=description)
        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for('list_projects'))

    return render_template('add_project.html')


# --- UPDATE: Edit an existing project ---
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    project = db.session.get(Project, id)

    if project is None:
        return 'Project not found', 404

    if request.method == 'POST':
        project.name = request.form['name']
        project.description = request.form.get('description', '')
        db.session.commit()

        return redirect(url_for('list_projects'))

    return render_template('edit_project.html', project=project)


# --- DELETE: Remove a project ---
@app.route('/delete/<int:id>')
def delete_project(id):
    project = db.session.get(Project, id)

    if project is None:
        return 'Project not found', 404

    db.session.delete(project)
    db.session.commit()

    return redirect(url_for('list_projects'))


# --- Initialise the database and run the app ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

You should also have these templates in your `templates/` folder:
- `base.html` : shared layout
- `projects.html` : list view with Edit/Delete buttons
- `add_project.html` : form to add projects
- `edit_project.html` : form to edit projects

---

## Part 1: Refactor into MVC

### What is MVC?

MVC stands for **Model-View-Controller**, a design pattern that separates your application into three components:

| Component | Responsibility | In Flask |
|-----------|---------------|----------|
| **Model** | Data structure and database logic | Python classes using SQLAlchemy |
| **View** | What the user sees | HTML templates (Jinja2) |
| **Controller** | Business logic, connects Model and View | Route functions and helper functions |

### Why refactor?

Your W4 code works, but everything is in one file. As applications grow, this becomes hard to maintain. By separating concerns:

- **Easier to navigate**: you know where to find things
- **Easier to maintain**: changes to one part don't break others
- **Easier to collaborate**: team members can work on different parts

### Our target folder structure

```
flask_project/
├── app.py                  # Slimmed down: Flask app + routes only
├── models/
│   ├── __init__.py         # Makes this a Python package
│   └── project.py          # Project model (moved from app.py)
├── controllers/
│   ├── __init__.py
│   └── projects.py         # Helper functions (if needed)
├── templates/
│   ├── base.html           # Already exists from W4
│   ├── projects.html       # Already exists from W4
│   ├── add_project.html    # Already exists from W4
│   └── edit_project.html   # Already exists from W4
└── instance/
    └── data.db             # Your existing database
```

### Step 1.1: Create the directory structure

Inside your existing project folder, create these new folders:

```
models/
controllers/
```

You can do this in VS Code's file explorer or via terminal:

```bash
mkdir models
mkdir controllers
```

**Note:** You already have a `templates/` folder and possibly an `instance/` folder containing `data.db`, leave those as they are.

### Step 1.2: Create the Project model file

We'll move the `Project` class out of `app.py` and into its own file.

---

**Step 1: Create the new file**

Create a new empty file: `models/project.py`

---

**Step 2: Find and CUT this code from app.py:**

```python
# CUT this from app.py:

# --- Define the Project model ---
class Project(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<Project {self.id}: {self.name}>'
```

---

**Step 3: Paste into models/project.py and add imports**

After pasting, add the imports at the top. Your `models/project.py` should now contain:

```python
# models/project.py

from flask_sqlalchemy import SQLAlchemy

# Create the db instance here, we'll import it elsewhere
db = SQLAlchemy()


class Project(db.Model):
    """Represents a software project in the database."""

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<Project {self.id}: {self.name}>'
```

**Key change:** We now create `db = SQLAlchemy()` in this file (without passing `app`). We'll connect it to the app later using `db.init_app(app)`.

### Step 1.3: Create the models package __init__.py

This file makes the `models` folder a Python package and provides convenient imports.

---

**Step 1: Create the new file**

Create a new file: `models/__init__.py`

---

**Step 2: Add this content to models/__init__.py:**

```python
# models/__init__.py

from .project import db, Project

__all__ = ['db', 'Project']
```

This lets us write `from models import db, Project` elsewhere in our code.

**What does `__all__` do?** It explicitly declares which names get exported when someone writes `from models import *`. It's optional but good practice. It documents which names are part of the public API.

### Step 1.4: Create the controllers package

Even though our routes will stay in `app.py`, we'll set up the controllers folder for helper functions. This keeps things organised.

---

**Step 1: Create the new file**

Create a new file: `controllers/__init__.py`

---

**Step 2: Add this content to controllers/__init__.py:**

```python
# controllers/__init__.py

# This file makes 'controllers' a Python package.
# We'll add helper functions here if needed.
```

### Step 1.5: Update app.py

Now we need to update `app.py` to:
- Remove the `Project` class (it's now in `models/project.py`)
- Import from our new models package
- Change how we initialise the database

---

**BEFORE: your app.py has the Project class and db = SQLAlchemy(app)**

---

**AFTER: app.py with imports updated and Project class removed:**

```python
# app.py (after refactoring)

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, redirect, url_for, abort
from models import db, Project

# --- Create the Flask application ---
app = Flask(__name__)

# --- Configure the database ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Initialise the database with the app ---
db.init_app(app)


# =============================================================================
# ROUTES (same as W4, all CRUD functionality preserved)
# =============================================================================

# --- READ: List all projects ---
@app.route('/')
def list_projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)


# --- CREATE: Add a new project ---
@app.route('/add', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')

        new_project = Project(name=name, description=description)
        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for('list_projects'))

    return render_template('add_project.html')


# --- UPDATE: Edit an existing project ---
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    project = db.session.get(Project, id)

    if project is None:
        abort(404)

    if request.method == 'POST':
        project.name = request.form['name']
        project.description = request.form.get('description', '')
        db.session.commit()

        return redirect(url_for('list_projects'))

    return render_template('edit_project.html', project=project)


# --- DELETE: Remove a project ---
@app.route('/delete/<int:id>')
def delete_project(id):
    project = db.session.get(Project, id)

    if project is None:
        abort(404)

    db.session.delete(project)
    db.session.commit()

    return redirect(url_for('list_projects'))


# =============================================================================
# RUN THE APPLICATION
# =============================================================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

**Key changes:**
1. Added `sys.path.insert(...)` to help Python find our packages
2. Changed import from `from flask_sqlalchemy import SQLAlchemy` to `from models import db, Project`
3. Removed `db = SQLAlchemy(app)` and replaced with `db.init_app(app)`
4. Removed the `Project` class (it's now in `models/project.py`)
5. Added `abort` to Flask imports for proper 404 handling
6. **All CRUD routes remain unchanged**: add, edit, delete all still work!

### Step 1.6: Verify the refactoring worked

Let's make sure everything still works after our refactoring.

**Your folder structure should now look like:**

```
flask_project/
├── app.py                  # Slimmed down (no Project class)
├── models/
│   ├── __init__.py
│   └── project.py          # Project class lives here now
├── controllers/
│   └── __init__.py         # Empty for now
├── templates/
│   ├── base.html
│   ├── projects.html
│   ├── add_project.html
│   └── edit_project.html
└── instance/
    └── data.db             # Your existing database
```

**Test it:**

```bash
python app.py
```

**Test all your existing functionality:**
- http://127.0.0.1:5000/ : Should show your projects list
- Click "Add New Project" : Should still work
- Click "Edit" on a project : Should still work
- Click "Delete" on a project : Should still work

**Checkpoint:** Give your tutor a thumbs up when your app starts without errors and all CRUD operations work.

---

## Part 2: Add New Routes

Now we'll add some new routes to our application:
- An **About page** (static route)
- A **Project detail page** (dynamic route)

### Types of routes

| Type | Example | Description |
|------|---------|-------------|
| **Static** | `/about` | Always returns the same content |
| **Dynamic** | `/projects/<id>` | Content depends on the URL parameter |

### Step 2.1: Create the About page template

---

**Step 1: Create the new file**

Create a new file: `templates/about.html`

---

**Step 2: Add this content**

```html
<!-- templates/about.html -->

{% extends "base.html" %}

{% block content %}
<h2>About Project Manager</h2>
<p>This is a simple project management application built with Flask
   as part of the Software Engineering & Agile module.</p>
<p>It demonstrates the <strong>Model-View-Controller (MVC)</strong> pattern
   and basic database operations using Flask-SQLAlchemy.</p>
<h3>Features</h3>
<ul>
    <li>View all projects</li>
    <li>Add new projects</li>
    <li>Edit existing projects</li>
    <li>Delete projects</li>
    <li>Organise projects by category</li>
</ul>
{% endblock %}
```

### Step 2.2: Create the Project detail page template

---

**Step 1: Create the new file**

Create a new file: `templates/project_detail.html`

---

**Step 2: Add this content**

```html
<!-- templates/project_detail.html -->

{% extends "base.html" %}

{% block content %}
<h2>{{ project.name }}</h2>
<p>{{ project.description or "No description provided." }}</p>
<p>
    <a href="{{ url_for('edit_project', id=project.id) }}" class="btn btn-edit">Edit</a>
    <a href="{{ url_for('delete_project', id=project.id) }}" class="btn btn-danger"
       onclick="return confirm('Are you sure you want to delete this project?');">Delete</a>
</p>
<p><a href="{{ url_for('list_projects') }}">&larr; Back to all projects</a></p>
{% endblock %}
```

### Step 2.3: Add the new routes to app.py

Add these two new routes to your `app.py`, **after the existing routes but before** the `if __name__ == '__main__':` block:

```python
# --- About page (static route) ---
@app.route('/about')
def about():
    """Display the about page."""
    return render_template('about.html')


# --- Project detail page (dynamic route) ---
@app.route('/projects/<int:id>')
def project_detail(id):
    """Display a single project by ID."""
    project = db.session.get(Project, id)
    if project is None:
        abort(404)
    return render_template('project_detail.html', project=project)
```

### Step 2.4: Update base.html navigation

Add a link to the About page in your navigation. Edit `templates/base.html` and find the `<nav>` section.

---

**BEFORE:**

```html
    <nav>
        <a href="{{ url_for('list_projects') }}">All Projects</a>
        <a href="{{ url_for('add_project') }}">Add New Project</a>
    </nav>
```

---

**AFTER:**

```html
    <nav>
        <a href="{{ url_for('list_projects') }}">All Projects</a>
        <a href="{{ url_for('add_project') }}">Add New Project</a>
        <a href="{{ url_for('about') }}">About</a>
    </nav>
```

### Step 2.5: Update projects.html to link to detail page

In the projects list, make the project name clickable. Edit `templates/projects.html`.

---

**BEFORE: the name column:**

```html
            <td>{{ project.name }}</td>
```

---

**AFTER: name links to detail page:**

```html
            <td><a href="{{ url_for('project_detail', id=project.id) }}">{{ project.name }}</a></td>
```

### Step 2.6: Test the new routes

```bash
python app.py
```

**Test:**
- http://127.0.0.1:5000/about : Should show the About page
- Click a project name in the list : Should show the detail page
- http://127.0.0.1:5000/projects/999 : Should show a 404 error

**Checkpoint:** Give your tutor a thumbs up when the new routes work.

---

## Part 3: Create a Category Model with Relationships

Real applications almost always have **related data**. We'll add a Category table and link it to Projects.

### How relationships work in SQLAlchemy

```
┌─────────────┐         ┌─────────────┐
│  Category   │         │   Project   │
├─────────────┤         ├─────────────┤
│ id (PK)     │◄────────│ category_id │ (FK)
│ name        │         │ id (PK)     │
└─────────────┘         │ name        │
                        │ description │
                        └─────────────┘
```

- One **Category** can have many **Projects** (one-to-many)
- Each **Project** belongs to one **Category** (via `category_id` foreign key)

### Step 3.1: Create the Category model

---

**Step 1: Create the new file**

Create a new file: `models/category.py`

---

**Step 2: Add this content:**

```python
# models/category.py

from .project import db


class Category(db.Model):
    """Represents a category for organising projects."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    # Relationship: a category has many projects
    # The 'backref' creates a .category attribute on Project objects
    projects = db.relationship('Project', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.id}: '{self.name}'>"
```

### Step 3.2: Update the Project model with a foreign key

Edit `models/project.py` to add the `category_id` column.

---

**BEFORE: models/project.py:**

```python
class Project(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<Project {self.id}: {self.name}>'
```

---

**AFTER: models/project.py with foreign key:**

```python
class Project(db.Model):
    """Represents a software project in the database."""

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    # Foreign key linking to the Category table
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

    def __repr__(self):
        return f'<Project {self.id}: {self.name}>'
```

### Step 3.3: Update models/__init__.py

Edit `models/__init__.py` to export the Category class.

---

**BEFORE:**

```python
# models/__init__.py (current)
from .project import db, Project

__all__ = ['db', 'Project']
```

---

**AFTER:**

```python
# models/__init__.py (with Category)
from .project import db, Project
from .category import Category

__all__ = ['db', 'Project', 'Category']
```

### Step 3.4: Create a seed script

We need to add the new Category table to our database and populate it with some categories. This script will update the database schema and add categories, your existing projects will be preserved.

---

**Step 1: Create the new file**

Create a new file: `seed.py` (in the root of your project, same level as `app.py`)

> **Extension opportunity:** After this workshop, try building full CRUD routes for categories: list, create, edit, delete. Great assessment practice!

---

**Step 2: Add this content:**

```python
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
        print("\nCategories already exist, skipping seed.")
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
```

**Note:** This script uses `db.create_all()` which only creates *new* tables, it won't delete your existing projects. Your W4 projects will still be there, just without categories assigned yet. You'll assign categories to them later using the web form.

### Step 3.5: Update app.py import

Edit the import line in `app.py` to include Category.

---

**BEFORE:**

```python
from models import db, Project
```

---

**AFTER:**

```python
from models import db, Project, Category
```

### Step 3.6: Run the seed script

```bash
python seed.py
```

You should see output like:
```
Database schema updated.

Categories created:
   [1] Web Apps
   [2] Data Science
   [3] Automation

Done!
```

**Checkpoint:** Give your tutor a thumbs up when you see the categories created. Your existing projects are still there, you'll assign categories to them in Part 4.

---

## Part 4: Update Templates and Routes for Categories

Now let's update the templates to display category information and add a category detail page.

### Step 4.1: Update projects.html to show categories

Add a Category column to the projects table. Edit `templates/projects.html`.

---

**BEFORE: the table header row:**

```html
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Description</th>
            <th>Actions</th>
        </tr>
```

---

**AFTER: with Category column:**

```html
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Category</th>
            <th>Description</th>
            <th>Actions</th>
        </tr>
```

---

**BEFORE: the table body row:**

```html
        <tr>
            <td>{{ project.id }}</td>
            <td><a href="{{ url_for('project_detail', id=project.id) }}">{{ project.name }}</a></td>
            <td>{{ project.description or "-" }}</td>
            <td>
                <a href="{{ url_for('edit_project', id=project.id) }}" class="btn btn-edit">Edit</a>
                <a href="{{ url_for('delete_project', id=project.id) }}" class="btn btn-danger"
                   onclick="return confirm('Are you sure?');">Delete</a>
            </td>
        </tr>
```

---

**AFTER: with Category column:**

```html
        <tr>
            <td>{{ project.id }}</td>
            <td><a href="{{ url_for('project_detail', id=project.id) }}">{{ project.name }}</a></td>
            <td>
                {% if project.category %}
                <a href="{{ url_for('category_detail', id=project.category.id) }}">
                    {{ project.category.name }}
                </a>
                {% else %}
                -
                {% endif %}
            </td>
            <td>{{ project.description or "-" }}</td>
            <td>
                <a href="{{ url_for('edit_project', id=project.id) }}" class="btn btn-edit">Edit</a>
                <a href="{{ url_for('delete_project', id=project.id) }}" class="btn btn-danger"
                   onclick="return confirm('Are you sure?');">Delete</a>
            </td>
        </tr>
```

### Step 4.2: Update project_detail.html to show category

Edit `templates/project_detail.html` to show the project's category.

---

**BEFORE:**

```html
{% block content %}
<h2>{{ project.name }}</h2>
<p>{{ project.description or "No description provided." }}</p>
```

---

**AFTER:**

```html
{% block content %}
<h2>{{ project.name }}</h2>
{% if project.category %}
<p><strong>Category:</strong>
    <a href="{{ url_for('category_detail', id=project.category.id) }}">
        {{ project.category.name }}
    </a>
</p>
{% endif %}
<p>{{ project.description or "No description provided." }}</p>
```

### Step 4.3: Create the category detail template

---

**Step 1: Create the new file**

Create a new file: `templates/category_detail.html`

---

**Step 2: Add this content**

```html
<!-- templates/category_detail.html -->

{% extends "base.html" %}

{% block content %}
<h2>{{ category.name }} Projects</h2>

{% if category.projects %}
<table>
    <thead>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Description</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for project in category.projects %}
        <tr>
            <td>{{ project.id }}</td>
            <td><a href="{{ url_for('project_detail', id=project.id) }}">{{ project.name }}</a></td>
            <td>{{ project.description or "-" }}</td>
            <td>
                <a href="{{ url_for('edit_project', id=project.id) }}" class="btn btn-edit">Edit</a>
                <a href="{{ url_for('delete_project', id=project.id) }}" class="btn btn-danger"
                   onclick="return confirm('Are you sure?');">Delete</a>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% else %}
<p>No projects in this category yet. <a href="{{ url_for('add_project') }}">Add one!</a></p>
{% endif %}

<p><a href="{{ url_for('list_projects') }}">&larr; Back to all projects</a></p>
{% endblock %}
```

### Step 4.4: Add the category route to app.py

Add this route to `app.py` (after the existing routes):

```python
# --- Category detail page ---
@app.route('/categories/<int:id>')
def category_detail(id):
    """Display all projects in a category."""
    category = db.session.get(Category, id)
    if category is None:
        abort(404)
    return render_template('category_detail.html', category=category)
```

### Step 4.5: Update add/edit forms to include category

We need to update the add and edit forms to allow selecting a category.

---

**Update templates/add_project.html**: add a category dropdown after the name field:

```html
<!-- templates/add_project.html -->

{% extends "base.html" %}

{% block content %}
<h2>Add a New Project</h2>

<form method="POST">
    <label for="name">Project Name (required):</label>
    <input type="text" id="name" name="name" required>

    <label for="category_id">Category (optional):</label>
    <select id="category_id" name="category_id">
        <option value="">-- No Category --</option>
        {% for category in categories %}
        <option value="{{ category.id }}">{{ category.name }}</option>
        {% endfor %}
    </select>

    <label for="description">Description (optional):</label>
    <textarea id="description" name="description" rows="3"></textarea>

    <button type="submit" class="btn btn-primary">Add Project</button>
</form>
{% endblock %}
```

---

**Update templates/edit_project.html**: add a category dropdown:

```html
<!-- templates/edit_project.html -->

{% extends "base.html" %}

{% block content %}
<h2>Edit Project: {{ project.name }}</h2>

<form method="POST">
    <label for="name">Project Name (required):</label>
    <input type="text" id="name" name="name" value="{{ project.name }}" required>

    <label for="category_id">Category (optional):</label>
    <select id="category_id" name="category_id">
        <option value="">-- No Category --</option>
        {% for category in categories %}
        <option value="{{ category.id }}" {% if project.category_id == category.id %}selected{% endif %}>
            {{ category.name }}
        </option>
        {% endfor %}
    </select>

    <label for="description">Description (optional):</label>
    <textarea id="description" name="description" rows="3">{{ project.description or "" }}</textarea>

    <button type="submit" class="btn btn-primary">Save Changes</button>
    <a href="{{ url_for('list_projects') }}" class="btn">Cancel</a>
</form>
{% endblock %}
```

### Step 4.6: Update the add/edit routes to handle categories

Update the `add_project` and `edit_project` routes in `app.py`.

---

**BEFORE: add_project route:**

```python
@app.route('/add', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')

        new_project = Project(name=name, description=description)
        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for('list_projects'))

    return render_template('add_project.html')
```

---

**AFTER: add_project with category support:**

```python
@app.route('/add', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        category_id = request.form.get('category_id')

        # Convert empty string to None
        if category_id == '':
            category_id = None
        else:
            category_id = int(category_id)

        new_project = Project(name=name, description=description, category_id=category_id)
        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for('list_projects'))

    categories = Category.query.all()
    return render_template('add_project.html', categories=categories)
```

---

**BEFORE: edit_project route:**

```python
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    project = db.session.get(Project, id)

    if project is None:
        abort(404)

    if request.method == 'POST':
        project.name = request.form['name']
        project.description = request.form.get('description', '')
        db.session.commit()

        return redirect(url_for('list_projects'))

    return render_template('edit_project.html', project=project)
```

---

**AFTER: edit_project with category support:**

```python
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    project = db.session.get(Project, id)

    if project is None:
        abort(404)

    if request.method == 'POST':
        project.name = request.form['name']
        project.description = request.form.get('description', '')
        category_id = request.form.get('category_id')

        # Convert empty string to None
        if category_id == '':
            project.category_id = None
        else:
            project.category_id = int(category_id)

        db.session.commit()

        return redirect(url_for('list_projects'))

    categories = Category.query.all()
    return render_template('edit_project.html', project=project, categories=categories)
```

### Step 4.7: Test the complete application

```bash
python app.py
```

**Test all functionality:**

1. **View the projects list**: http://127.0.0.1:5000/
   - You should see a new "Category" column (showing "-" for your existing projects)

2. **Assign categories to your existing projects:**
   - Click "Edit" on one of your W4 projects
   - Select a category from the dropdown
   - Click "Save Changes"
   - Repeat for your other projects

3. **Test the category links:**
   - Click a category name in the projects list
   - You should see only the projects in that category

4. **Test creating a new project with a category:**
   - Click "Add New Project"
   - Fill in the form and select a category
   - Verify it appears in the list with the correct category

5. **Test the project detail page:**
   - Click a project name
   - The category should be displayed and linked

**Checkpoint:** Can you create, edit, and delete projects with categories?

---

## Part 5: Practice Exercises

1. **Add a new category**: Edit `seed.py` to add a "Mobile Apps" category, then re-run it
2. **Create a new project**: Use the web form to create a "FitTracker" project in the Mobile Apps category
3. **Verify the relationship**: Click the category name to see only projects in that category
4. **(Stretch)**: Add a route that lists all categories with their project counts

---

## Summary

| Concept | What you did |
|---------|---------------|
| **Refactoring** | Reorganised existing code into MVC structure |
| **MVC Structure** | models/, controllers/, templates/ folders |
| **Static Routes** | `/about` returns same content every time |
| **Dynamic Routes** | `/projects/<id>` fetches data based on URL |
| **404 Handling** | `abort(404)` for missing resources |
| **One-to-Many** | Categories → Projects via foreign key |
| **Relationships** | `project.category` and `category.projects` |
| **Full CRUD** | All create, read, update, delete operations work with categories |

---

## Extension: Full Category CRUD

Build complete CRUD routes for categories:
- `GET /categories` : List all categories
- `GET /categories/new` : Show form to create category
- `POST /categories` : Save new category
- `GET /categories/<id>/edit` : Show form to edit category
- `POST /categories/<id>` : Save category changes
- `GET /categories/<id>/delete` : Delete category

This is excellent practice for your assessment!

---

## Reference: Final File States

### Final folder structure

```
flask_project/
├── app.py
├── seed.py
├── models/
│   ├── __init__.py
│   ├── project.py
│   └── category.py
├── controllers/
│   └── __init__.py
├── templates/
│   ├── base.html
│   ├── projects.html
│   ├── add_project.html
│   ├── edit_project.html
│   ├── project_detail.html
│   ├── category_detail.html
│   └── about.html
└── instance/
    └── data.db
```

### Final app.py

```python
# app.py (final)

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, redirect, url_for, abort
from models import db, Project, Category

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# --- READ: List all projects ---
@app.route('/')
def list_projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)


# --- CREATE: Add a new project ---
@app.route('/add', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        category_id = request.form.get('category_id')

        if category_id == '':
            category_id = None
        else:
            category_id = int(category_id)

        new_project = Project(name=name, description=description, category_id=category_id)
        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for('list_projects'))

    categories = Category.query.all()
    return render_template('add_project.html', categories=categories)


# --- UPDATE: Edit an existing project ---
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    project = db.session.get(Project, id)

    if project is None:
        abort(404)

    if request.method == 'POST':
        project.name = request.form['name']
        project.description = request.form.get('description', '')
        category_id = request.form.get('category_id')

        if category_id == '':
            project.category_id = None
        else:
            project.category_id = int(category_id)

        db.session.commit()

        return redirect(url_for('list_projects'))

    categories = Category.query.all()
    return render_template('edit_project.html', project=project, categories=categories)


# --- DELETE: Remove a project ---
@app.route('/delete/<int:id>')
def delete_project(id):
    project = db.session.get(Project, id)

    if project is None:
        abort(404)

    db.session.delete(project)
    db.session.commit()

    return redirect(url_for('list_projects'))


# --- About page ---
@app.route('/about')
def about():
    return render_template('about.html')


# --- Project detail page ---
@app.route('/projects/<int:id>')
def project_detail(id):
    project = db.session.get(Project, id)
    if project is None:
        abort(404)
    return render_template('project_detail.html', project=project)


# --- Category detail page ---
@app.route('/categories/<int:id>')
def category_detail(id):
    category = db.session.get(Category, id)
    if category is None:
        abort(404)
    return render_template('category_detail.html', category=category)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

### Final models/project.py

```python
# models/project.py (final)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Project(db.Model):
    """Represents a software project in the database."""

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

    def __repr__(self):
        return f'<Project {self.id}: {self.name}>'
```

### Final models/category.py

```python
# models/category.py (final)

from .project import db


class Category(db.Model):
    """Represents a category for organising projects."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    projects = db.relationship('Project', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.id}: '{self.name}'>"
```

### Final models/__init__.py

```python
# models/__init__.py (final)

from .project import db, Project
from .category import Category

__all__ = ['db', 'Project', 'Category']
```

### Final seed.py

```python
# seed.py (final)

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
        print("\nCategories already exist, skipping seed.")
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
```
