from fastapi import APIRouter

from app.api.v1 import auth, projects, agents, skills, tools, models, workflows, executions, runs, role_templates, code_runtime

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
api_router.include_router(agents.router, prefix="/agents", tags=["Agents"])
api_router.include_router(skills.router, prefix="/skills", tags=["Skills"])
api_router.include_router(tools.router, prefix="/tools", tags=["Tools"])
api_router.include_router(models.router, prefix="/models", tags=["Models"])
api_router.include_router(workflows.router, prefix="/workflows", tags=["Workflows"])
api_router.include_router(executions.router, prefix="/executions", tags=["Executions"])
api_router.include_router(runs.router, prefix="/runs", tags=["Runs"])
api_router.include_router(role_templates.router, prefix="/role-templates", tags=["RoleTemplates"])
api_router.include_router(code_runtime.router, tags=["CodeRuntime"])
