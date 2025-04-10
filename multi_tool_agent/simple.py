from google.adk.agents import Agent

root_agent = Agent(
    name="simple_assistant",
    model="gemini-2.0-flash-exp", # Or your preferred Gemini model
    instruction="You are a helpful assistant.",
    description="A helpful assistant.",
)