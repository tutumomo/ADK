# python ./multi_tool_agent/agent.py

import asyncio
from dotenv import load_dotenv
from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams, StdioServerParameters

# Load environment variables from .env file if needed
load_dotenv()

# --- Step 1: 獲取工具的異步函數 ---
async def get_tools_async():
    """從MCP服務器獲取工具"""
    print("嘗試連接到MCP服務器...")
    tools, exit_stack = await MCPToolset.from_server(
        connection_params=StdioServerParameters(
            command='python3',
            args=["-m", "mcp_server_fetch"],
        )
    )
    print("MCP Toolset 創建成功.")
    # MCP 需要維持與本地MCP服務器的連接
    # exit_stack 管理這個連接的清理
    return tools, exit_stack

# --- Step 2: 創建代理的異步函數 ---
async def get_agent_async():
    """創建一個配備了MCP服務器工具的ADK代理"""
    tools, exit_stack = await get_tools_async()
    print(f"從MCP服務器獲取了 {len(tools)} 個工具.")

    root_agent = LlmAgent(
        model='gemini-2.0-flash',  # 根據可用性調整模型名稱
        name='fetch_assistant',
        instruction='使用可用工具幫助用戶從網頁中提取內容.',
        tools=tools,  # 將MCP工具提供給ADK代理
    )
    return root_agent, exit_stack

# --- Step 3: 主執行邏輯 ---
async def async_main():
    session_service = InMemorySessionService()
    artifacts_service = InMemoryArtifactService()

    session = session_service.create_session(
        state={}, app_name='mcp_fetch_app', user_id='user_fetch'
    )

    # 設置查詢
    query = "從 https://example.com 提取內容"
    print(f"用戶查詢: '{query}'")
    content = types.Content(role='user', parts=[types.Part(text=query)])

    root_agent, exit_stack = await get_agent_async()

    runner = Runner(
        app_name='mcp_fetch_app',
        agent=root_agent,
        artifact_service=artifacts_service,
        session_service=session_service,
    )

    print("運行代理中...")
    events_async = runner.run_async(
        session_id=session.id, user_id=session.user_id, new_message=content
    )

    async for event in events_async:
        print(f"收到事件: {event}")

    # 關鍵清理步驟: 確保MCP服務器進程連接已關閉
    print("關閉MCP服務器連接...")
    await exit_stack.aclose()
    print("清理完成.")

if __name__ == '__main__':
    try:
        asyncio.run(async_main())
    except Exception as e:
        print(f"發生錯誤: {e}")

