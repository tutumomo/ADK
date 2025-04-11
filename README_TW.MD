# Agent Development Kit (ADK)

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

<html>
    <h1 align="center">
      <img src="assets/agent-development-kit.png" width="256"/>
    </h1>
    <h3 align="center">
      一個開源的、以代碼為先的 Python 工具包，用於構建、評估和部署具有靈活性和控制性的高級 AI 代理。
    </h3>
    <h3 align="center">
      重要連結：
      <a href="https://google.github.io/adk-docs/">文檔</a> &
      <a href="https://github.com/google/adk-samples">示例</a>。
    </h3>
</html>

Agent Development Kit (ADK) 旨在為尋求細粒度控制和靈活性的開發者提供服務，當他們構建與 Google Cloud 服務緊密集成的高級 AI 代理時。它允許您直接在代碼中定義代理行為、協調和工具使用，從而實現強大的調試、版本控制和部署 - 從您的筆記本電腦到雲端。

---

## ✨ 主要功能

* **以代碼為先的開發：** 定義代理、工具和協調邏輯，以實現最大控制、可測試性和版本控制。
* **多代理架構：** 通過組合多個專業代理在靈活的層次結構中構建模塊化和可擴展的應用程序。
* **豐富的工具生態系統：** 使用預建工具、定制 Python 函數、API 規範或整合現有工具來賦予代理多樣化的能力。
* **靈活的協調：** 使用內建代理定義工作流程以實現可預測的管道，或利用 LLM 驅動的動態路由來實現自適應行為。
* **集成的開發體驗：** 使用 CLI 和可視化網頁 UI 在本地開發、測試和調試。
* **內建評估：** 通過評估響應質量和逐步執行軌跡來衡量代理性能。
* **準備部署：** 將您的代理容器化並部署到任何地方 - 使用 Vertex AI Agent Engine、Cloud Run 或 Docker 進行擴展。
* **原生流式支持：** 使用原生支持的雙向流式傳輸（文本和音頻）構建實時、互動的體驗。
* **狀態、記憶與工件：** 管理短期對話上下文，配置長期記憶，並處理文件上傳/下載。
* **可擴展性：** 使用回調深度自定義代理行為，並輕鬆整合第三方工具和服務。

## 🚀 安裝

您可以使用 `pip` 安裝 ADK：

```bash
pip install google-adk
```

## 🏁 開始使用

創建您的第一個代理（`my_agent/agent.py`）：

```python
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
```

創建 `my_agent/__init__.py`：

```python
# my_agent/__init__.py
from . import agent
```

通過 CLI 運行它（從包含 `my_agent` 的目錄中）：

```bash
adk run my_agent
```

或者從包含 `my_agent` 資料夾的資料夾啟動 Web UI：

```bash
adk web
```

如需完整的逐步指南，請查看 [快速入門](https://google.github.io/adk-docs/get-started/quickstart/) 或 [示例代理](https://github.com/google/adk-samples)。

## 📚 資源

探索完整的文檔，了解構建、評估和部署代理的詳細指南：

*   **[開始使用](https://google.github.io/adk-docs/get-started/)**
*   **[瀏覽示例代理](https://github.com/google/adk-samples)**
*   **[評估代理](https://google.github.io/adk-docs/evaluate/)**
*   **[部署代理](https://google.github.io/adk-docs/deploy/)**
*   **[API 參考](https://google.github.io/adk-docs/api-reference/)**

## 🤝 貢獻

我們歡迎來自社區的貢獻！無論是錯誤報告、功能請求、文檔改進還是代碼貢獻，請查看我們的 [**貢獻指南**](./CONTRIBUTING.md) 以開始。

## 📄 許可證

本項目在 Apache 2.0 許可證下授權 - 詳見 [LICENSE](LICENSE) 文件。

---

*祝您代理開發愉快！*