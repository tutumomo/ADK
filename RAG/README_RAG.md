# 文件檢索代理程式

## 概觀

此代理程式旨在回答與您上傳到 Vertex AI RAG 引擎的文件相關的問題。它利用 Vertex AI RAG 引擎的檢索增強生成 (RAG) 功能來擷取相關的文件片段和程式碼參考，然後由 LLM (Gemini) 進行綜合，以提供包含引用的資訊性答案。

![RAG 架構](RAG_architecture.png)

此圖表概述了代理程式的工作流程，旨在提供資訊豐富且具備上下文感知的回應。使用者查詢由代理程式開發套件處理。LLM 判斷是否需要外部知識 (RAG 語料庫)。如果需要，`VertexAiRagRetrieval` 工具會從已設定的 Vertex RAG 引擎語料庫中擷取相關資訊。然後，LLM 將此擷取的資訊與其內部知識相結合，以生成準確的答案，包括指向來源文件 URL 的引用。

## 代理程式詳細資訊
| 屬性         | 詳細資訊                                                                                                                                                                                             |
| :---------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **互動類型** | 對話式                                                                                                                                                                                      |
| **複雜度**    | 中等
| **代理程式類型**    | 單一代理程式                                                                                                                                                                                        |
| **元件**    | 工具、RAG、評估                                                                                                                                                                               |
| **垂直領域**      | 水平                                                                                                                                                                               |
### 代理程式架構

![RAG](RAG_workflow.png)


### 主要功能

*   **檢索增強生成 (RAG):** 利用 [Vertex AI RAG 引擎](https://cloud.google.com/vertex-ai/generative-ai/docs/rag-overview) 來擷取相關文件。
*   **引用支援:** 為擷取的內容提供準確的引用，格式為 URL。
*   **清晰的指示:** 遵守嚴格的準則，以提供基於事實的答案和正確的引用。

## 設定與安裝說明
### 先決條件

*   **Google Cloud 帳戶:** 您需要一個 Google Cloud 帳戶。
*   **Python 3.9+:** 確保您已安裝 Python 3.9 或更新版本。
*   **Poetry:** 依照官方 Poetry 網站上的說明安裝 Poetry：[https://python-poetry.org/docs/](https://python-poetry.org/docs/)
*   **Git:** 確保您已安裝 git。

### 使用 Poetry 進行專案設定

1.  **複製儲存庫:**

    ```bash
    git clone https://github.com/google/adk-samples.git
    cd google-adk-samples/agents/RAG
    ```

2.  **使用 Poetry 安裝依賴項:**

    ```bash
    poetry install
    ```

    此命令會讀取 `pyproject.toml` 檔案，並將所有必要的依賴項安裝到由 Poetry 管理的虛擬環境中。

3.  **啟動 Poetry Shell:**

    ```bash
    poetry env activate
    ```

    這會啟動虛擬環境，讓您可以在專案的環境中執行命令。
    請確保環境已啟動。如果沒有，您也可以透過以下方式啟動：

     ```bash
    source .venv/bin/activate
    ```
4.  **設定環境變數:**
    將檔案 ".env example" 重新命名為 ".env"
    依照檔案中的步驟設定環境變數。

5. **設定語料庫:**
    如果您在 Vertex AI RAG 引擎中已有現有的語料庫，請在您的 .env 檔案中設定語料庫資訊。例如：RAG_CORPUS='projects/123/locations/us-central1/ragCorpora/456'。

    如果您尚未設定語料庫，請依照「如何將我的檔案上傳到我的 RAG 語料庫」一節進行操作。`prepare_corpus_and_data.py` 指令碼將自動建立語料庫 (如果需要)，並使用建立或擷取的語料庫的資源名稱更新您 `.env` 檔案中的 `RAG_CORPUS` 變數。

#### 如何將我的檔案上傳到我的 RAG 語料庫

`rag/shared_libraries/prepare_corpus_and_data.py` 指令碼可協助您設定 RAG 語料庫並上傳初始文件。預設情況下，它會下載 Alphabet 的 2024 年 10-K PDF 檔案，並將其上傳到新的語料庫。

1.  **使用您的 Google Cloud 帳戶進行驗證:**
    ```bash
    gcloud auth application-default login
    ```

2.  **在您的 `.env` 檔案中設定環境變數:**
    確保您的 `.env` 檔案 (從 `.env.example` 複製) 已設定以下變數：
    ```
    GOOGLE_CLOUD_PROJECT=your-project-id
    GOOGLE_CLOUD_LOCATION=your-location  # 例如：us-central1
    ```

3.  **設定並執行準備指令碼:**
    *   **若要使用預設行為 (上傳 Alphabet 的 10K PDF):**
        只需執行指令碼：
        ```bash
        python rag/shared_libraries/prepare_corpus_and_data.py
        ```
        這將建立一個名為 `Alphabet_10K_2024_corpus` 的語料庫 (如果不存在)，並上傳從指令碼中指定的 URL 下載的 PDF 檔案 `goog-10-k-2024.pdf`。

    *   **若要從 URL 上傳不同的 PDF:**
        a. 開啟 `rag/shared_libraries/prepare_corpus_and_data.py` 檔案。
        b. 修改指令碼頂部的以下變數：
           ```python
           # --- 請填寫您的設定 ---
           # ... 專案和位置從 .env 讀取 ...
           CORPUS_DISPLAY_NAME = "您的語料庫名稱"  # 視需要變更
           CORPUS_DESCRIPTION = "您的語料庫描述" # 視需要變更
           PDF_URL = "https://path/to/your/document.pdf"  # 指向您的 PDF 文件的 URL
           PDF_FILENAME = "your_document.pdf"  # 語料庫中檔案的名稱
           # --- 指令碼開始 ---
           ```
        c. 執行指令碼：
           ```bash
           python rag/shared_libraries/prepare_corpus_and_data.py
           ```

    *   **若要上傳本機 PDF 檔案:**
        a. 開啟 `rag/shared_libraries/prepare_corpus_and_data.py` 檔案。
        b. 視需要修改 `CORPUS_DISPLAY_NAME` 和 `CORPUS_DESCRIPTION` 變數 (請參閱上方)。
        c. 修改指令碼底部的 `main()` 函數，以使用您的本機檔案詳細資訊直接呼叫 `upload_pdf_to_corpus`：
           ```python
           def main():
             initialize_vertex_ai()
             corpus = create_or_get_corpus() # 使用 CORPUS_DISPLAY_NAME 和 CORPUS_DESCRIPTION

             # 將您的本機 PDF 上傳到語料庫
             local_file_path = "/path/to/your/local/file.pdf" # 設定正確的路徑
             display_name = "您的檔案名稱.pdf" # 設定所需的顯示名稱
             description = "您的檔案描述" # 設定描述

             # 上傳前確保檔案存在
             if os.path.exists(local_file_path):
                 upload_pdf_to_corpus(
                     corpus_name=corpus.name,
                     pdf_path=local_file_path,
                     display_name=display_name,
                     description=description
                 )
             else:
                 print(f"錯誤：在 {local_file_path} 找不到本機檔案")

             # 列出語料庫中的所有檔案
             list_corpus_files(corpus_name=corpus.name)
           ```
        d. 執行指令碼：
           ```bash
           python rag/shared_libraries/prepare_corpus_and_data.py
           ```

有關在 Vertex RAG 引擎中管理資料的更多詳細資訊，請參閱[官方文件頁面](https://cloud.google.com/vertex-ai/generative-ai/docs/rag-quickstart)。

## 執行代理程式
您可以使用終端機中的 ADK 命令來執行代理程式。
從根專案目錄：

1.  在 CLI 中執行代理程式：

    ```bash
    adk run rag
    ```

2.  使用 ADK Web UI 執行代理程式：
    ```bash
    adk web
    ```
    從下拉式選單中選取 RAG


### 互動範例
以下是使用者可能如何與代理程式互動的快速範例：

**範例 1：文件資訊檢索**

使用者：Alphabet 的 2024 年 10-K 報告中提到的主要業務部門有哪些？

代理程式：根據 Alphabet 的 2024 年 10-K 報告，主要業務部門為：
1. Google 服務 (包括 Google 搜尋、YouTube、Google 地圖、Play 商店)
2. Google Cloud (提供雲端運算服務、資料分析和 AI 解決方案)
3. 其他投資 (包括用於自動駕駛技術的 Waymo)
[來源：goog-10-k-2024.pdf]

## 評估代理程式

可以從 `RAG` 目錄使用 `pytest` 模組執行評估：

```
poetry run pytest eval
```

### 評估流程

評估框架包含三個主要元件：

1. **test_eval.py**: 主要的測試指令碼，用於協調評估流程。它使用 Google ADK 的 `AgentEvaluator` 來針對測試資料集執行代理程式，並根據預先定義的標準評估其效能。

2. **conversation.test.json**: 包含一系列結構化為對話的測試案例。每個測試案例包括：
   - 使用者查詢 (例如，關於 Alphabet 的 10-K 報告的問題)
   - 預期的工具使用情況 (代理程式應呼叫哪些工具以及使用哪些參數)
   - 參考答案 (代理程式應提供的理想回應)

3. **test_config.json**: 定義評估標準和閾值：
   - `tool_trajectory_avg_score`: 衡量代理程式使用適當工具的程度
   - `response_match_score`: 衡量代理程式的回應與參考答案的匹配程度

當您執行評估時，系統會：
1. 從 conversation.test.json 載入測試案例
2. 將每個查詢傳送給代理程式
3. 將代理程式的工具使用情況與預期的工具使用情況進行比較
4. 將代理程式的回應與參考答案進行比較
5. 根據 test_config.json 中的標準計算分數

此評估有助於確保代理程式正確利用 RAG 功能來檢索相關資訊，並生成包含正確引用的準確回應。

## 部署代理程式

可以使用以下命令將代理程式部署到 Vertex AI Agent Engine：

```
python deployment/deploy.py
```

部署代理程式後，您將能夠讀取以下 INFO 記錄訊息：

```
已成功將代理程式部署到 Vertex AI Agent Engine，資源名稱：projects/<PROJECT_NUMBER>/locations/us-central1/reasoningEngines/<AGENT_ENGINE_ID>
```

請記下您的 Agent Engine 資源名稱並相應地更新 `.env` 檔案，因為這對於測試遠端代理程式至關重要。

您也可以修改部署指令碼以符合您的使用案例。

## 測試已部署的代理程式

部署代理程式後，請依照下列步驟進行測試：

1. **更新環境變數:**
   - 開啟您的 `.env` 檔案。
   - 當您部署代理程式時，`AGENT_ENGINE_ID` 應該已由 `deployment/deploy.py` 指令碼自動更新。請確認其設定正確：
     ```
     AGENT_ENGINE_ID=projects/<PROJECT_NUMBER>/locations/us-central1/reasoningEngines/<AGENT_ENGINE_ID>
     ```

2. **授予 RAG 語料庫存取權限:**
   - 確保您的 `.env` 檔案已正確設定以下變數：
     ```
     GOOGLE_CLOUD_PROJECT=your-project-id
     RAG_CORPUS=projects/<project-number>/locations/us-central1/ragCorpora/<corpus-id>
     ```
   - 執行權限指令碼：
     ```bash
     chmod +x deployment/grant_permissions.sh
     ./deployment/grant_permissions.sh
     ```
   此指令碼將：
   - 從您的 `.env` 檔案讀取環境變數
   - 建立具有 RAG 語料庫查詢權限的自訂角色
   - 將必要的權限授予 AI Platform Reasoning Engine Service Agent

3. **測試遠端代理程式:**
   - 執行測試指令碼：
     ```bash
     python deployment/run.py
     ```
   此指令碼將：
   - 連線到您已部署的代理程式
   - 傳送一系列測試查詢
   - 以適當的格式顯示代理程式的回應

測試指令碼包含有關 Alphabet 的 10-K 報告的範例查詢。您可以修改 `deployment/run.py` 中的查詢以測試已部署代理程式的不同方面。

## 自訂

### 自訂代理程式
您可以為代理程式自訂系統指示，並新增更多工具以滿足您的需求，例如 Google 搜尋。

### 自訂 Vertex RAG 引擎
您可以閱讀更多關於[官方 Vertex RAG 引擎文件](https://cloud.google.com/vertex-ai/generative-ai/docs/rag-quickstart)的詳細資訊，以了解自訂語料庫和資料的更多細節。


### 插入其他檢索來源
您還可以整合您偏好的檢索來源，以增強代理程式的功能。例如，您可以無縫地將現有的 `VertexAiRagRetrieval` 工具替換或擴充為使用 Vertex AI Search 或任何其他檢索機制的工具。這種靈活性讓您可以根據特定的資料來源和檢索需求來調整代理程式。