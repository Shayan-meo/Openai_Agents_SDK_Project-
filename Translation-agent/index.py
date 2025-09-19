from agents import (
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
)
import asyncio
from agents import Agent, Runner
from dotenv import load_dotenv
from agents import set_default_openai_client, set_tracing_disabled
load_dotenv()
import os
Gemini_Api_Key = os.getenv("Gemini_Api_Key")


if not Gemini_Api_Key:
    raise ValueError("Gemini_Api_Key environment variable not set")
# print("API Key found")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=Gemini_Api_Key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

set_default_openai_client(external_client)
set_tracing_disabled(True)


spanish_agent = Agent(
    name="spanish_agent",
    instructions="An agent that translates English text to Spanish.",
    handoff_description="an english text to Spanish translator",
    model=model,
)
french_agent = Agent(
    name="french_agent",
    instructions="An agent that translates English text to French.",
    handoff_description="an english text to French translator",
    model=model,
)

italian_agent = Agent(
    name="italian_agent",
    instructions="An agent that translates English text to Italian.",
    handoff_description="an english text to Italian translator",
    model=model,
)
main_agent= Agent(
    name="main_agent",
    instructions=(
        "you are a translation agent. you ues the tool  ginve to you to translate text"
        "if asked for multiple translations, use the tools multiple times" 
        "if the user asks you to translate to Spanish, use the Spanish Translator tool"
        ), 
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="useful for translating English text to Spanish"
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="useful for translating English text to French"
        ),
        italian_agent.as_tool(
            tool_name="translate_to_italian",
            tool_description="useful for translating English text to Italian"
        )
    ] ,
    model=model,
)


async def main():
    msg = input("Hi! What would you like translated, and to which languages? ")

    orchestrator_result = await Runner.run(main_agent, msg)
    print(f"\n\nFinal response:\n{orchestrator_result.final_output}")

    
if __name__ == "__main__":
    asyncio.run(main())
