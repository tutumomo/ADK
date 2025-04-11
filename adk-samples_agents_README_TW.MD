# 範例代理

這個資料夾包含了 [Agent Development Kit](https://github.com/google/adk-python) (ADK) 的代理範例。

這個目錄中的每個資料夾都包含不同的代理範例。

## 開始使用

1. **前置條件：**

   * 確保你已經安裝並配置了 Agent Development Kit (ADK)。參見 [ADK 快速入門指南](https://google.github.io/adk-docs/get-started/quickstart/)。
   * 安裝了 Python 3.9+ 和 [Poetry](https://python-poetry.org/docs/#installation)。
   * 訪問 Google Cloud (Vertex AI) 和/或 Gemini API 金鑰（依據代理的不同，請參閱各代理的 README）。

2. **運行範例代理：**

   * 導航到特定代理的目錄（例如，`cd agents/llm-auditor`）。
   * 將 `.env.example` 檔案複製到 `.env` 並填寫所需的環境變數（API 金鑰、項目 ID 等）。參閱代理的特定 README 以獲取所需變數的詳細信息。
   * 使用 Poetry 安裝依賴：`poetry install`
   * 按照代理的 `README.md` 中的指示來運行它（例如，使用 `adk run .` 或 `adk web`）。

## 代理類別

查看下面的代理範例，按類別組織：

| 代理名稱                                  | 用例                                                                                                                              | 標籤 | 互動類型 | 複雜度 | 代理類型   | 垂直領域                      |
| :------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------- | :-: | :--------------- | :--------- | :----------- | :---------------------------- |
| [品牌搜尋優化](brand-search-optimization) | 通過分析頂級搜索結果來豐富產品數據，解決“空值與低回收率”/“零結果”搜索問題，並識別產品數據中的缺口。                                 |   多代理, 自定義工具, 範例商店, Fast API, BigQuery 連接, Google 搜索 API, 電腦使用   | 工作流程 | 簡單 | 多代理 | 零售                        |
| [Cymbal 家居與園藝客戶服務代理](customer-service) | 客戶服務、產品選擇、訂單管理，適用於家居改善、園藝及相關用品                                |  自定義工具, 異步工具, 外部系統調用, 實時流, 多模態   | 對話         | 高級     | 單代理       | 零售                        |
| [數據科學代理](data-science) | 設計用於高級數據分析的多代理系統                                                                          |  函數工具 (Python), 代理工具, NL2SQL, 結構化數據, 數據庫   | 對話 | 高級 | 多代理 | 橫向                    |
| [FOMC 研究代理](fomc-research) | 市場事件分析                                                                                                                   |   視頻分析, 摘要, 報告生成  | 工作流程 | 高級 | 多代理 | 金融服務            |
| [LLM 審計員](llm-auditor)                   | 聊天機器人響應驗證，內容審計                                                                                         |   Gemini 與 Google 搜索, 多代理  | 工作流程         | 簡單       | 多代理  | 橫向                    |
| [個人化購物](personalized-shopping) | 產品推薦                                                                                                               | 電子商務, 個人化代理, 購物助手, 單代理, 產品推薦, 產品發現, 聊天機器人    | 對話         | 簡單        | 單代理     | 電子商務                    |
| [Vertex AI 檢索代理](RAG) | RAG 驅動的代理 / 回答與上傳到 Vertex AI RAG 引擎的文件相關的問題，提供帶有來源材料引用的信息性回答。                              |  RAG 引擎   | 工作流程              | 中級        | 單代理       | 橫向                    |
| [旅行禮賓](travel-concierge) | 旅行禮賓，數位任務助理                                                                                               |   函數工具 (Python), 自定義工具, 代理工具, 輸入和輸出模式, 可更新上下文, 動態指令  | 對話 | 高級 | 多代理 | 旅行                        |

## 使用本倉庫中的代理

本節提供了一般指導，說明如何運行、測試、評估並可能部署本倉庫中找到的代理範例。雖然核心步驟相似，但**每個代理都有其自己的特定要求和詳細指示，請參閱其專用 `README.md` 檔案。**

**始終參閱特定代理目錄中的 `README.md`（例如，`agents/fomc-research/README.md`）以獲取最準確和詳細的步驟。**

這裡是一個你可以期待的一般工作流程：

1. **選擇代理：**從上表中選擇一個與你的興趣或用例相符的代理。
2. **導航到代理目錄：**打開你的終端並進入代理的主目錄：
   ```bash
   cd agents/<agent-name> 
   # 例如：cd agents/fomc-research
   ```
3. **查看代理的 README：**這是最關鍵的一步。打開該目錄中的 `README.md` 檔案。它將包含：
   * 代理的目的和架構的詳細概述。
   * 特定前置條件（例如，API 金鑰、雲服務、數據庫設置）。
   * 設置和安裝的逐步指示。
   * 當地運行代理的命令。
   * 運行評估的指示（如適用）。
   * 運行測試的指示（如適用）。
   * 部署的步驟（如適用）。

4. **設置和配置：**
   * **前置條件：**確保你已經滿足了主要“開始使用”部分中列出的通用前置條件*和*代理 README 中提到的任何特定前置條件。
   * **依賴：**使用 Poetry 安裝代理的特定 Python 依賴（通常從代理的主目錄中運行此命令）：
       ```bash
       poetry install
       ```
   * **環境變數：**大多數代理需要通過環境變數進行配置。將 `.env.example` 檔案複製到代理目錄中的 `.env` 並填入你的特定值（API 金鑰、項目 ID 等）。參閱代理的 README 以獲取所需變數的詳細信息。你可能需要將這些變數載入到你的 shell 環境中（例如，使用 `source .env` 或 `set -o allexport; . .env; set +o allexport` 在 bash 中）。

5. **本地運行代理：**
   * 代理通常可以使用 ADK CLI 或 ADK Dev UI 在本地運行以進行測試和互動。具體命令可能略有不同（例如，確切的運行目錄），所以請檢查代理的 README。
   * **CLI：**通常涉及從代理的*核心代碼*目錄中運行 `adk run .`（例如，`agents/fomc-research/fomc_research/`）。
       ```bash
       # 示例（檢查代理的 README 以獲取確切路徑）
       cd agents/fomc-research/fomc_research/ 
       adk run . 
       ```
   * **ADK Dev UI：**通常涉及從代理的*主*目錄中運行 `adk web .`（例如，`agents/fomc-research/`）。
       ```bash
       # 示例（檢查代理的 README 以獲取確切路徑）
       cd agents/fomc-research/
       adk web
       ```
       然後，在你的瀏覽器中打開提供的 URL 並從下拉選單中選擇代理。

6. **評估代理：**
   * 許多代理包括一個 `eval/` 目錄，包含用於評估性能的腳本和數據。
   * 代理的 README 將解釋如何運行這些評估（例如，`python eval/test_eval.py`）。這有助於驗證代理在特定任務上的有效性。

7. **測試代理組件：**
   * `tests/` 目錄通常包含單元或集成測試（例如，針對自定義工具）。
   * 這些確保個別代碼組件正確運行。
   * 代理的 README 可能提供如何運行這些測試的指示，通常使用像 `pytest` 這樣的框架。

8. **部署代理：**
   * 一些代理設計用於部署，通常到 [Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview)。
   * `deployment/` 目錄包含必要的腳本（如 `deploy.py`）和配置檔案。
   * 部署通常需要特定的 Google Cloud 設置（項目 ID、啟用的 API、權限）。代理的 README 和 `deployment/` 資料夾中的腳本提供詳細指示，類似於 `fomc-research` 代理文檔中展示的示例。

通過遵循每個代理的 `README.md` 中的特定指示，你可以有效地設置、運行、評估、測試並可能部署這些多樣的示例。

## 代理目錄結構
這裡展示的每個代理都按以下方式組織：

```bash
├── agent-name
│   ├── agent_name/
│   │   ├── shared_libraries/               # 包含工具的輔助函數資料夾
│   │   ├── sub_agents/                     # 每個子代理的資料夾
│   │   │   │   ├── tools/                  # 子代理的工具資料夾
│   │   │   │   ├── agent.py                # 子代理的核心邏輯
│   │   │   │   └── prompt.py               # 子代理的提示
│   │   │   └── ...                         # 更多子代理    
│   │   ├── __init__.py                     # 初始化代理
│   │   ├── tools/                          # 包含路由代理使用的工具代碼
│   │   ├── agent.py                        # 包含代理的核心邏輯
│   │   ├── prompt.py                       # 包含代理的提示
│   ├── deployment/                         # 部署到 Agent Engine
│   ├── eval/                               # 包含評估方法的資料夾
│   ├── tests/                              # 包含工具單元測試的資料夾
│   ├── agent_pattern.png                   # 代理模式的圖表
│   ├── .env.example                        # 存儲代理特定環境變數
│   ├── pyproject.toml                      # 項目配置
│   └── README.md                           # 提供代理的概述
```

### 一般結構

每個代理的根目錄位於 `agents/` 下的自己的目錄中。例如，`llm-auditor` 代理位於 `agents/llm-auditor/`。

#### 目錄分解

1. **`agent_name/` (核心代理代碼)**: 
   * 這個目錄包含代理的核心邏輯。
   * **`shared_libraries/`**: （可選）包含多個子代理共享的代碼。
   * **`sub_agents/`**: 包含子代理的定義和邏輯。
       * 每個子代理都有自己的目錄（例如，`critic/` 和 `reviser/` 在 `llm-auditor` 中）。
       * **`tools/`**: 包含特定於子代理的任何自定義工具。
       * **`agent.py`**: 定義子代理的行為，包括其模型、工具和指示。
       * **`prompt.py`**: 包含用於指導子代理行為的提示。
   * **`__init__.py`**: 一個初始化檔案，導入來自資料夾的 `agent.py`，用於標記 `agent_name` 目錄為 Python 包。
   * **`tools/`**: 包含主代理使用的任何自定義工具。
   * **`agent.py`**: 定義主代理的行為，包括其子代理、模型、工具和指示。
   * **`prompt.py`**: 包含用於指導主代理行為的提示。
   
   請注意，初始資料夾名稱是用 "-" 連接詞，而核心邏輯存儲在同名但用 "_" 連接詞的資料夾中（例如，`llm_auditor`）。這是由於 poetry 強加的項目結構。

2. **`deployment/`**

   * 包含部署代理到如 Vertex AI Agent Engine 這樣的平台所需的腳本和檔案。
   * 通常在這裡找到 `deploy.py` 腳本，處理部署過程。

3. **`eval/`**

   * 包含用於評估代理性能的數據和腳本。
   * 測試數據（例如，`.test.json` 檔案）和評估腳本（例如，`test_eval.py`）通常位於此處。

4. **`tests/`**

   * 包含代理的單元和集成測試。
   * 測試檔案（例如，`test_agents.py`）用於驗證代理的功能。

5. **`agent_pattern.png`**

   * 一個視覺圖表，說明代理的架構，包括其子代理及其互動。

6. **`.env.example`**

   * 一個示例檔案，顯示運行代理所需的環境變數。
   * 用戶應該將此檔案複製到 `.env` 並填入他們的特定值。

7. **`pyproject.toml`**

   * 包含項目元數據、依賴和構建系統配置。
   * 由 Poetry 管理依賴。

8. **`README.md`**

   * 提供特定於代理的詳細文檔，包括其目的、設置指示、使用示例和自定義選項。

## 示例：`llm-auditor`

`llm-auditor` 代理有效地展示了這個結構。它有：

* 一個核心 `llm_auditor/` 目錄。
* 子代理在 `llm_auditor/sub_agents/` 中，例如 `critic/` 和 `reviser/`。
* 部署腳本在 `deployment/` 中。
* 評估數據和腳本在 `eval/` 中。
* 測試在 `tests/` 中。
* 一個 `.env.example` 檔案。
* 一個 `pyproject.toml` 檔案。
* 一個 `README.md` 檔案。