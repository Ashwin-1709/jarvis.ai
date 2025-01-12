import os
from constants import *
from tools import tools
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver


class Jarvis:
    """
    A class to represent the Jarvis AI agent.
    This class initializes the AI model, sets up the prompt, and creates the agent executor.
    """

    def __init__(self) -> None:
        """
        Initializes the Jarvis instance.
        Sets up the AI model, prompt, and agent executor.
        """
        self.model = ChatGoogleGenerativeAI(
            api_key=os.getenv("GEMINI_API_KEY"), model=MODEL
        )

        self.setup_prompt()
        self.create_agent()

        print(GREET)

    def setup_prompt(self) -> None:
        """
        Sets up the initial prompt and memory for the agent.
        Initializes the memory saver and sets the system prompt.
        """
        self.memory = MemorySaver()
        self.system_prompt = SYSTEM_PROMPT

    def create_agent(self) -> None:
        """
        Creates the agent executor with the specified model,
        tools, state modifier, and checkpointer.
        Also sets up the configuration for the agent.
        """
        self.agent_executor = create_react_agent(
            self.model,
            tools,
            state_modifier=self.system_prompt,
            checkpointer=self.memory,
        )
        self.config = {"configurable": {"thread_id": "test-thread"}}

    def run(self) -> None:
        """
        Runs the agent in an infinite loop, taking user input and invoking the agent executor.
        Prints the input and output messages.
        """
        while True:
            query = input("> ")
            messages = self.agent_executor.invoke(
                {"messages": [("human", query)]}, config=self.config
            )
            print(messages["messages"][-1].content)


def main():
    load_dotenv()
    assistant = Jarvis()
    assistant.run()


if __name__ == "__main__":
    main()
