from app.runtime.agent_runner import AgentRunner


class NormalAgentRunner:
    def __init__(self):
        self.agent_runner = AgentRunner()

    def run(self, prompt_result, model_config):
        return self.agent_runner.run(prompt_result, model_config)
