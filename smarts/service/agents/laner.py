from smarts.core.agent import AgentSpec, AgentPolicy
from smarts.core.agent_interface import AgentInterface, AgentType


class LanerPolicy(AgentPolicy):
    def act(self, obs):
        return "keep_lane"


AGENT_ID = "Agent-007"
agent_spec = AgentSpec(
    interface=AgentInterface.from_type(AgentType.Laner, max_episode_steps=None),
    policy_builder=LanerPolicy,
)
agent_specs = {AGENT_ID: agent_spec}
agent_interfaces = {
    agent_id: agent.interface for agent_id, agent in agent_specs.items()
}
