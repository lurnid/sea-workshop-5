# controllers/__init__.py (final)

from .projects import (
    get_all_projects,
    get_project_by_id,
    create_project,
    update_project,
    delete_project
)

__all__ = [
    'get_all_projects',
    'get_project_by_id',
    'create_project',
    'update_project',
    'delete_project'
]
