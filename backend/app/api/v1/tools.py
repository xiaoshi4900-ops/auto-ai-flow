from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.api.deps import get_current_user_id
from app.db.models.tool import Tool
from app.schemas.tool import ToolResponse, ToolListResponse

router = APIRouter()


@router.get("", response_model=ToolListResponse)
def list_tools(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), db: Session = Depends(get_db_session)):
    query = db.query(Tool)
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return ToolListResponse(total=total, items=[ToolResponse.model_validate(t) for t in items])
