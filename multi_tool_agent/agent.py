## 🔥 調用ollama模型
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

# 創建使用Ollama Gemma模型的代理
root_agent = LlmAgent(
    model=LiteLlm(model="ollama/gemma3:4b"),  # Correct format for Ollama models
    name="helpful_agent",
    description=(
        "a helpful assistant."
    ),
    instruction=(
        "You are a helpful assistant. You should always response in traditional chinese"
    ),
)
