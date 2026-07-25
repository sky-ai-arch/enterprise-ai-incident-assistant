from incident_assistant.domain.interfaces.agent import Agent


class RuntimeRegistry:

    def __init__(self):
        self._agents: dict[str, Agent] = {}

    def register(
        self,
        agent: Agent,
    ) -> None:

        self._agents[agent.name] = agent

    def get(
        self,
        name: str,
    ) -> Agent:

        return self._agents[name]