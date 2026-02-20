# controllers/projects.py (final)

from models import db, Project


def get_all_projects():
    return Project.query.all()


def get_project_by_id(project_id):
    return db.session.get(Project, project_id)


def create_project(name, description=None, category_id=None):
    new_project = Project(name=name, description=description, category_id=category_id)
    db.session.add(new_project)
    db.session.commit()
    return new_project


def update_project(project_id, new_name=None, new_description=None, new_category_id=None):
    project = db.session.get(Project, project_id)
    if project is None:
        return None
    if new_name is not None:
        project.name = new_name
    if new_description is not None:
        project.description = new_description
    if new_category_id is not None:
        project.category_id = new_category_id
    db.session.commit()
    return project


def delete_project(project_id):
    project = db.session.get(Project, project_id)
    if project is None:
        return False
    db.session.delete(project)
    db.session.commit()
    return True
