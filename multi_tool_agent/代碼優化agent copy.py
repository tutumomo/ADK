# 導入必要的庫
from google.adk.agents.sequential_agent import SequentialAgent  # 導入順序代理
from google.adk.agents.llm_agent import LlmAgent  # 導入LLM代理
from google.adk.agents import Agent  # 導入基礎代理類
from google.genai import types  # 導入類型定義
from google.adk.sessions import InMemorySessionService  # 導入內存會話服務
from google.adk.runners import Runner  # 導入運行器
from google.adk.tools import FunctionTool  # 導入函數工具，用於創建自定義工具

# --- 常量定義 ---
APP_NAME = "code_pipeline_app"  # 應用名稱
USER_ID = "dev_user_01"  # 用戶ID
SESSION_ID = "pipeline_session_01"  # 會話ID
GEMINI_MODEL = "gemini-2.0-flash-exp"  # 使用的Gemini模型

# --- 1. 定義代碼處理管道的各個階段子代理 ---
# 代碼編寫代理
# 接收初始規格說明(來自用戶查詢)並編寫代碼
code_writer_agent = LlmAgent(
    name="CodeWriterAgent",  # 代理名稱
    model=GEMINI_MODEL,  # 使用的模型
    instruction="""你是一個代碼編寫AI。
    根據用戶的請求，編寫初始Python代碼。
    只輸出原始代碼塊。
    """,  # 代理指令（中文版）
    description="根據規格說明編寫初始代碼。",  # 代理描述
    # 將其輸出(生成的代碼)存儲到會話狀態中
    # 鍵名為'generated_code'
    output_key="generated_code"  # 輸出鍵，用於存儲代理輸出到會話狀態
)

# 代碼審查代理
# 讀取上一個代理生成的代碼(從狀態中讀取)並提供反饋
code_reviewer_agent = LlmAgent(
    name="CodeReviewerAgent",  # 代理名稱
    model=GEMINI_MODEL,  # 使用的模型
    instruction="""你是一個代碼審查AI。
    審查會話狀態中鍵名為'generated_code'的Python代碼。
    提供關於潛在錯誤、風格問題或改進的建設性反饋。
    注重清晰度和正確性。
    僅輸出審查評論。
    """,  # 代理指令（中文版）
    description="審查代碼並提供反饋。",  # 代理描述
    # 將其輸出(審查評論)存儲到會話狀態中
    # 鍵名為'review_comments'
    output_key="review_comments"  # 輸出鍵，用於存儲代理輸出到會話狀態
)

# 代碼重構代理
# 獲取原始代碼和審查評論(從狀態中讀取)並重構代碼
code_refactorer_agent = LlmAgent(
    name="CodeRefactorerAgent",  # 代理名稱
    model=GEMINI_MODEL,  # 使用的模型
    instruction="""你是一個代碼重構AI。
    獲取會話狀態鍵'generated_code'中的原始Python代碼
    以及會話狀態鍵'review_comments'中的審查評論。
    重構原始代碼以解決反饋並提高其質量。
    僅輸出最終的、重構後的代碼塊。
    """,  # 代理指令（中文版）
    description="根據審查評論重構代碼。",  # 代理描述
    # 將其輸出(重構的代碼)存儲到會話狀態中
    # 鍵名為'refactored_code'
    output_key="refactored_code"  # 輸出鍵，用於存儲代理輸出到會話狀態
)

# --- 2. 創建順序代理 ---
# 這個代理通過按順序運行子代理來編排流水線
code_pipeline_agent = SequentialAgent(
    name="CodePipelineAgent",  # 順序代理名稱
    sub_agents=[code_writer_agent, code_reviewer_agent, code_refactorer_agent]
    # 子代理將按提供的順序運行：編寫器 -> 審查器 -> 重構器
)

# --- 3. 創建一個函數作為工具 ---
def process_code_request(request: str) -> str:
    """
    使用代碼處理管道處理用戶的代碼請求。

    Args:
        request (str): 用戶的代碼請求，如"創建一個計算加法的函數"

    Returns:
        str: 處理後的最終代碼
    """
    print(f"處理代碼請求: {request}")
    # 這個函數實際上不會被執行，而是被LLM用來理解它應該如何使用code_pipeline_agent
    # 真正的執行是通過root_agent對code_pipeline_agent的委託實現的
    return "最終的代碼將在這裡返回"

# --- 4. 創建根代理 ---
root_agent = Agent(
    name="CodeAssistant",  # 根代理名稱
    model=GEMINI_MODEL,  # 使用的模型
    instruction="""你是一個代碼助手AI。
    你的角色是通過三步流水線幫助用戶改進代碼：
    1. 根據規格說明編寫初始代碼
    2. 審查代碼以發現問題和改進
    3. 根據審查反饋重構代碼

    當用戶請求代碼幫助時，使用code_pipeline_agent來處理請求。
    將最終的、重構後的代碼作為你的響應呈現給用戶。
    """,  # 根代理指令（中文版）
    description="通過編寫-審查-重構流水線改進代碼的助手。",  # 根代理描述
    # 不在工具中添加code_pipeline_agent，而是作為子代理
    tools=[],  # 這裡可以為空，或者添加其他工具
    sub_agents=[code_pipeline_agent]  # 將code_pipeline_agent作為子代理
)

# 會話和運行器設置
session_service = InMemorySessionService()  # 創建內存會話服務
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)  # 創建會話
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)  # 創建運行器

# 代理交互函數
def call_agent(query):
    """
    調用代理並處理用戶查詢

    Args:
        query (str): 用戶的查詢文本
    """
    content = types.Content(role='user', parts=[types.Part(text=query)])  # 創建用戶內容
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)  # 運行代理
    for event in events:  # 遍歷事件
        if event.is_final_response():  # 如果是最終響應
            final_response = event.content.parts[0].text  # 獲取響應文本
            print("代理響應: ", final_response)  # 打印響應

# 調用代理進行測試
call_agent("執行數學加法")  # 測試查詢
