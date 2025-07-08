
# Import the MCP client adapter to connect with the weather MCP tool server
from langchain_mcp_adapters.client import MultiServerMCPClient

# Import a pre-built LangGraph agent (ReAct logic) for tool reasoning
from langgraph.prebuilt import create_react_agent

# Import ChatGroq model wrapper for using Groq's LLMs (e.g., Qwen)
from langchain_groq import ChatGroq

# Used to load environment variables (e.g., GROQ_API_KEY)
from dotenv import load_dotenv
load_dotenv()  # Load .env file values into the environment

# Import asyncio to run the asynchronous workflow
import asyncio

# Main asynchronous function that executes the AI agent logic
async def main():
    # Define the MCP tool server configuration for weather
    client = MultiServerMCPClient(
        {
            "weather": {
                "url": "http://localhost:8000/mcp",  # Weather tool server URL
                "transport": "streamable_http",      # Transport protocol
            }
        }
    )

    # Load GROQ API key into environment for use by ChatGroq
    import os
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    # Discover available tools from the MCP server
    tools = await client.get_tools()

    # Load the Qwen model from Groq
    model = ChatGroq(model="qwen-qwq-32b")

    # Create the LangGraph ReAct agent with tools and model
    agent = create_react_agent(model, tools)

    # Step 1: Ask the agent for current weather in Karachi
    weather_response = await agent.ainvoke({
        "messages": [
            {"role": "user", "content": "Will it rain in karachi in upcoming days ?"}
        ]
    })
    print("Weather response:", weather_response['messages'][-1].content)

# Run the async workflow
asyncio.run(main())
