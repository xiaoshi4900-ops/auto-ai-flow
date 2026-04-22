import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.api.deps import get_current_user_id
from app.db.models.role_template import RoleTemplate
from app.schemas.role_template import RoleTemplateListResponse, RoleTemplateListItem, RoleTemplateResponse, CodeExecutionPolicySchema
from app.core.exceptions import NotFoundException

router = APIRouter()


@router.get("", response_model=RoleTemplateListResponse)
def list_role_templates(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    templates = db.query(RoleTemplate).filter(RoleTemplate.enabled == True).all()
    items = [
        RoleTemplateListItem(
            id=t.id,
            key=t.key,
            name=t.name,
            execution_mode=t.execution_mode,
        )
        for t in templates
    ]
    return RoleTemplateListResponse(items=items)


@router.get("/{template_id}", response_model=RoleTemplateResponse)
def get_role_template(template_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    tpl = db.query(RoleTemplate).filter(RoleTemplate.id == template_id).first()
    if not tpl:
        raise NotFoundException("RoleTemplate", error_code="ROLE_TEMPLATE_NOT_FOUND")

    policy = None
    if tpl.policy_config:
        try:
            policy_data = json.loads(tpl.policy_config)
            policy = CodeExecutionPolicySchema(**policy_data)
        except (json.JSONDecodeError, Exception):
            policy = None

    return RoleTemplateResponse(
        id=tpl.id,
        key=tpl.key,
        name=tpl.name,
        category=tpl.category,
        description=tpl.description,
        execution_mode=tpl.execution_mode,
        default_role_name=tpl.default_role_name,
        default_model_id=tpl.default_model_id,
        default_skill_ids=json.loads(tpl.default_skill_ids) if tpl.default_skill_ids else [],
        default_tool_ids=json.loads(tpl.default_tool_ids) if tpl.default_tool_ids else [],
        default_code_policy=policy,
        is_builtin=tpl.is_builtin,
        enabled=tpl.enabled,
    )
