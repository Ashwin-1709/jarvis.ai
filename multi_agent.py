""" Multi Agent Proof of concept - WIP."""

import os
from constants import (
    MODEL,
    DATETIME_AGENT_SYSTEM_PROMPT,
    CALENDAR_AGENT_SYSTEM_PROMPT,
    COMMUNICATOR_SYSTEM_PROMPT,
    HUMAN_AGENT_PROMPT,
    SUPERVISOR_PROMPT,
    GREET,
)
from dotenv import load_dotenv
import operator
from agent_creator import create_tool_agent
from typing import TypedDict, Sequence, Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import datetime_agent_tools, calendar_agent_tools
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel
from langchain_core.output_parsers import JsonOutputParser
from langgraph.graph import StateGraph, END
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.output_parsers import JsonOutputParser

from enum import Enum
import functools


members = ["DateTime", "Calendar", "Communicate", "HumanClarification"]


class MultiAgent:
    """
    A class to represent a multi-agent system.
    This class initializes various agents and sets up the supervisor agent.
    """

    def __init__(self) -> None:
        """
        Initializes the MultiAgent instance.
        Sets up the agents, supervisor agent, and graph.
        """
        load_dotenv()
        self.model = ChatGoogleGenerativeAI(
            api_key=os.getenv("GEMINI_API_KEY"), model=MODEL
        )

        self.config = {"configurable": {"thread_id": "test-thread"}}
        self.setup_agents()
        self.setup_supervisor_agent()
        self.setup_graph()

    def setup_agents(self) -> None:
        """
        Sets up the datetime agent, calendar agent, communicator agent, and human clarification agent.
        """

        # DateTime Agent
        self.datetime_agent = create_tool_agent(
            llm=self.model,
            tools=datetime_agent_tools,
            system_prompt=DATETIME_AGENT_SYSTEM_PROMPT,
        )

        # Calendar Agent
        self.calendar_agent = create_tool_agent(
            llm=self.model,
            tools=calendar_agent_tools,
            system_prompt=CALENDAR_AGENT_SYSTEM_PROMPT,
        )

        # Communicator Agent
        self.communicator_agent_prompt = PromptTemplate(
            template=COMMUNICATOR_SYSTEM_PROMPT,
            input_variables=["agent_history"],
        )

        system_message_prompt = SystemMessagePromptTemplate(
            prompt=self.communicator_agent_prompt
        )
        self.communicator_system_prompt = ChatPromptTemplate.from_messages(
            [
                system_message_prompt,
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        self.comms_agent = self.communicator_system_prompt | self.model

        # Human Clarification Agent
        self.human_clarification_agent_prompt = PromptTemplate(
            template=HUMAN_AGENT_PROMPT, input_variables=["agent_history"]
        )
        human_message_prompt = SystemMessagePromptTemplate(
            prompt=self.human_clarification_agent_prompt
        )
        self.human_clarification_system_prompt = ChatPromptTemplate.from_messages(
            [human_message_prompt, MessagesPlaceholder(variable_name="messages")]
        )
        self.human_agent = self.human_clarification_system_prompt | self.model

    def setup_supervisor_agent(self) -> None:
        """
        Sets up the supervisor agent which decides the next agent to process.
        """
        self.member_options = {member: member for member in members}

        MemberEnum = Enum("MemberEnum", self.member_options)

        # force Supervisor to pick from options defined above
        # return a dictionary specifying the next agent to call
        # under key next.
        class SupervisorOutput(BaseModel):
            # defaults to calendar agent
            next: MemberEnum = MemberEnum.Calendar

        system_prompt = SUPERVISOR_PROMPT
        # Supervisor is an LLM node. It just picks the next agent to process
        # and decides when the work is completed

        supervisor_parser = JsonOutputParser(pydantic_object=SupervisorOutput)

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
                MessagesPlaceholder(variable_name="agent_history"),
            ]
        ).partial(
            options=str(members),
            members=", ".join(members),
            format_instructions=supervisor_parser.get_format_instructions(),
        )

        self.supervisor_chain = prompt | self.model | supervisor_parser

    def setup_graph(self) -> None:
        """
        Sets up the graph for the multi-agent system.
        """

        # For agents in the crew
        def crew_nodes(state, crew_member, name):
            # read the last message in the message history.
            input = {
                "messages": [state["messages"][-1]],
                "agent_history": state["agent_history"],
            }
            result = crew_member.invoke(input)
            # add response to the agent history.
            return {
                "agent_history": [
                    AIMessage(
                        content=result["output"],
                        additional_kwargs={
                            "intermediate_steps": result["intermediate_steps"]
                        },
                        name=name,
                    )
                ]
            }

        def comms_node(state):
            # read the last message in the message history.
            input = {
                "messages": [state["messages"][-1]],
                "agent_history": state["agent_history"],
            }
            result = self.comms_agent.invoke(input)
            # respond back to the user.
            return {"messages": [result]}

        def human_node(state):
            # read the last message message in the message history.
            input = {
                "messages": [state["messages"][-1]],
                "agent_history": state["agent_history"],
            }
            result = self.human_agent.invoke(input)
            # respond back to the user.
            return {"messages": [result]}

        # The agent state is the input to each node in the graph
        class AgentState(TypedDict):
            # The annotation tells the graph that new messages will always
            # be added to the current states
            messages: Annotated[Sequence[BaseMessage], operator.add]
            # The 'next' field indicates where to route to next
            next: str

            agent_history: Annotated[Sequence[BaseMessage], operator.add]

        self.workflow = StateGraph(AgentState)

        self.datetime_node = functools.partial(
            crew_nodes, crew_member=self.datetime_agent, name="DateTime"
        )

        self.calendar_node = functools.partial(
            crew_nodes, crew_member=self.calendar_agent, name="Calendar"
        )

        self.workflow.add_node("DateTime", self.datetime_node)
        self.workflow.add_node("Calendar", self.calendar_node)

        self.workflow.add_node("Communicate", comms_node)
        self.workflow.add_node("HumanClarification", human_node)

        self.workflow.add_node("Supervisor", self.supervisor_chain)

        # set Supervisor as entrypoint to the graph.
        self.workflow.set_entry_point("Supervisor")

        # add one edge for each of the tool agents
        self.workflow.add_edge("DateTime", "Supervisor")
        self.workflow.add_edge("Calendar", "Supervisor")
        self.workflow.add_edge("HumanClarification", "Supervisor")

        # end loop at communication agent.
        self.workflow.add_edge("Communicate", END)

        # The supervisor populates the "next" field in the graph state
        # which routes to a node or finishes

        self.workflow.add_conditional_edges(
            "Supervisor", lambda x: x["next"], self.member_options
        )

        self.graph = self.workflow.compile(
            checkpointer=MemorySaver(), interrupt_after=["HumanClarification"]
        )

    def run(self) -> None:
        """
        Runs the multi-agent system in an infinite loop, taking user input and invoking the supervisor agent.
        """
        print(GREET)
        while True:
            query = input("> ")
            for s in self.graph.stream(
                {"messages": [HumanMessage(content=query)]}, config=self.config
            ):
                if "__end__" not in s:
                    print(s)
                    print("----")


def main() -> None:
    agent = MultiAgent()
    agent.run()


if __name__ == "__main__":
    main()
