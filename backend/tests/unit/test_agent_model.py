from app.db.models.agent import Agent, agent_skill_assoc, agent_tool_assoc
from app.db.models.project import Project
from app.db.models.user import User
from app.db.models.skill import Skill
from app.db.models.tool import Tool


def _setup(db):
    user = User(username="agentuser", email="agent@e.com", hashed_password="h")
    db.add(user)
    db.commit()
    project = Project(name="TestProject", owner_id=user.id)
    db.add(project)
    db.commit()
    return user, project


def test_agent_create(db):
    user, project = _setup(db)
    agent = Agent(name="TestAgent", project_id=project.id, role_name="assistant")
    db.add(agent)
    db.commit()
    assert agent.id is not None
    assert agent.project_id == project.id


def test_agent_belongs_to_project(db):
    user, project = _setup(db)
    agent = Agent(name="A1", project_id=project.id, role_name="assistant")
    db.add(agent)
    db.commit()
    assert agent.project_id == project.id


def test_agent_skill_association(db):
    user, project = _setup(db)
    skill = Skill(name="test_skill", description="test", prompt_template="tpl", is_builtin=True)
    db.add(skill)
    db.commit()
    agent = Agent(name="A2", project_id=project.id, role_name="assistant")
    db.add(agent)
    db.commit()
    db.execute(agent_skill_assoc.insert().values(agent_id=agent.id, skill_id=skill.id))
    db.commit()
    result = db.execute(agent_skill_assoc.select().where(agent_skill_assoc.c.agent_id == agent.id)).fetchall()
    assert len(result) == 1


def test_agent_tool_association(db):
    user, project = _setup(db)
    tool = Tool(name="test_tool", description="test", tool_type="function", config="{}", is_builtin=True)
    db.add(tool)
    db.commit()
    agent = Agent(name="A3", project_id=project.id, role_name="assistant")
    db.add(agent)
    db.commit()
    db.execute(agent_tool_assoc.insert().values(agent_id=agent.id, tool_id=tool.id))
    db.commit()
    result = db.execute(agent_tool_assoc.select().where(agent_tool_assoc.c.agent_id == agent.id)).fetchall()
    assert len(result) == 1
