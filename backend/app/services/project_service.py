from sqlalchemy.orm import Session

from app.db.repositories.project_repo import ProjectRepository
from app.schemas.project import ProjectCreateRequest, ProjectUpdateRequest, ProjectResponse, ProjectListResponse
from app.core.exceptions import NotFoundException, ForbiddenException


class ProjectService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ProjectRepository(db)

    def create(self, req: ProjectCreateRequest, owner_id: int) -> ProjectResponse:
        project = self.repo.create(name=req.name, owner_id=owner_id, description=req.description, default_model_id=req.default_model_id)
        return ProjectResponse.model_validate(project)

    def get(self, project_id: int, user_id: int) -> ProjectResponse:
        project = self.repo.get_by_id(project_id)
        if not project:
            raise NotFoundException("Project")
        if project.owner_id != user_id:
            raise ForbiddenException("Not project owner")
        return ProjectResponse.model_validate(project)

    def list_projects(self, user_id: int, page: int = 1, page_size: int = 20) -> ProjectListResponse:
        items, total = self.repo.list_by_owner(user_id, page, page_size)
        return ProjectListResponse(total=total, items=[ProjectResponse.model_validate(p) for p in items])

    def update(self, project_id: int, req: ProjectUpdateRequest, user_id: int) -> ProjectResponse:
        project = self.repo.get_by_id(project_id)
        if not project:
            raise NotFoundException("Project")
        if project.owner_id != user_id:
            raise ForbiddenException("Not project owner")
        updated = self.repo.update(project, **req.model_dump(exclude_unset=True))
        return ProjectResponse.model_validate(updated)

    def delete(self, project_id: int, user_id: int) -> None:
        project = self.repo.get_by_id(project_id)
        if not project:
            raise NotFoundException("Project")
        if project.owner_id != user_id:
            raise ForbiddenException("Not project owner")
        self.repo.soft_delete(project)
