# my_agent/agent.py
from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="search_assistant",
    model="gemini-2.0-flash-exp", # 或您偏好的 Gemini 模型
    instruction="您是一個有幫助的助手。當需要時使用 Google 搜索來回答用戶問題。",
    description="一個可以搜索網絡的助手。",
    tools=[google_search]
)