from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.api.deps import get_current_user_id
from app.db.models.skill import Skill
from app.schemas.skill import SkillResponse, SkillListResponse

router = APIRouter()


@router.get("", response_model=SkillListResponse)
def list_skills(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), db: Session = Depends(get_db_session)):
    query = db.query(Skill)
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return SkillListResponse(total=total, items=[SkillResponse.model_validate(s) for s in items])
