from sqlalchemy.orm import Session

from app.db.models.project import Project


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, project_id: int) -> Project | None:
        return self.db.query(Project).filter(Project.id == project_id, Project.is_deleted == False).first()

    def list_by_owner(self, owner_id: int, page: int = 1, page_size: int = 20) -> tuple[list[Project], int]:
        query = self.db.query(Project).filter(Project.owner_id == owner_id, Project.is_deleted == False)
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    def create(self, name: str, owner_id: int, description: str | None = None, default_model_id: int | None = None) -> Project:
        project = Project(name=name, owner_id=owner_id, description=description, default_model_id=default_model_id)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def update(self, project: Project, **kwargs) -> Project:
        for key, value in kwargs.items():
            if value is not None and hasattr(project, key):
                setattr(project, key, value)
        self.db.commit()
        self.db.refresh(project)
        return project

    def soft_delete(self, project: Project) -> Project:
        project.is_deleted = True
        self.db.commit()
        return project
