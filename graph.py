from langgraph.graph import StateGraph, START, END

from typing import TypedDict
from agents.supervisor import supervisor_agent
from agents.aggregator import aggregator_agent
from agents.investment_advisor import investment_advisor
import constants

supervisor = supervisor_agent()
aggregator = aggregator_agent()

# worker agents
investment_advisor_agent = investment_advisor()

class AgentState(TypedDict):
    user_input: str
    supervisor_agent: str
    planner_agent: str
    investment_advisor: str
    aggregator_agent: str

def supervisor_flow(state: AgentState) -> dict:
    user_input = state["user_input"]
    response = supervisor.supervise(user_input=user_input)
    return {constants.AGENT_STATE_SUPERVISOR_AGENT: response[constants.AGENT_STATE_SUPERVISOR_AGENT]}

def planner_router(state):
    nodes = []
    if "investment_advisor" in state[constants.AGENT_STATE_SUPERVISOR_AGENT]:
        nodes.append("investment_advisor")
    else:
        nodes.append("aggregator_agent")
    return nodes

def investment_advisor(state: AgentState) -> dict:
    user_input = state[constants.AGENT_STATE_USER_INPUT]
    response = investment_advisor_agent.investment_advice(user_input)
    return {constants.AGENT_STATE_INVESTMENT_ADVISOR: response[constants.AGENT_STATE_INVESTMENT_ADVISOR]}

def aggregator_flow(state: AgentState) -> dict:
    response = ""
    if "investment_advisor" in state[constants.AGENT_STATE_SUPERVISOR_AGENT]:
        response = state[constants.AGENT_STATE_INVESTMENT_ADVISOR]
        user_input = state["user_input"]
        result = aggregator.combine(user_input, response)
        response = result[constants.AGENT_STATE_AGGREGATOR_AGENT]
    if len(response) == 0:
        return {constants.AGENT_STATE_AGGREGATOR_AGENT: "Apologies I don't have any information in this topic"}
    return {constants.AGENT_STATE_AGGREGATOR_AGENT: response}

def create_workflow():
    builder = StateGraph(AgentState)

    builder.add_node("supervisor_agent", supervisor_flow)
    builder.add_node("investment_advisor", investment_advisor)
    builder.add_node("aggregator_agent", aggregator_flow)

    builder.add_edge(START, "supervisor_agent")
    builder.add_conditional_edges(
        "supervisor_agent",
        planner_router,
        {
            "investment_advisor": "investment_advisor",
            "aggregator_agent": "aggregator_agent"
        }
    )
    builder.add_edge("investment_advisor", "aggregator_agent")
    builder.add_edge("aggregator_agent", END)

    return builder.compile()

app = create_workflow()

