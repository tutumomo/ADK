# FOMC 研究代理程式

FOMC 研究代理程式使用多代理程式、多模態架構，結合工具使用、即時網路存取和外部資料庫整合，以產生關於聯邦公開市場委員會 (FOMC) 最新會議的詳細分析報告。此代理程式展示了一個多階段、非對話式的代理程式工作流程，而非對話式的使用者互動。

## 概觀

聯邦公開市場委員會 (FOMC) 是美國政府負責制定利率政策的機構。來自 FOMC 會議的聲明和新聞稿受到全球金融市場參與者的密切關注和徹底分析。

此代理程式展示了如何使用多代理程式架構來產生關於金融市場事件（例如聯準會會議）的詳細分析報告。FOMC 研究代理程式與其他代理程式略有不同，因為它基本上是非對話式的——代理程式的大部分工作是透過個別子代理程式之間的來回互動進行的。必要時，它會向使用者詢問關鍵資訊，但通常在沒有人工互動的情況下運作。

這是代理程式產生分析所遵循的高階工作流程（請注意，步驟 3，「檢閱記者會影片」，仍在開發中）。
![FOMC 研究代理程式工作流程](<FOMC_Research_Agent_Workflow.png>)

## 代理程式詳細資訊
FOMC 研究代理程式的主要功能包括：

| 功能 | 描述 |
| --- | --- |
| *互動類型* | 工作流程 |
| *複雜度* | 進階 |
| *代理程式類型* | 多代理程式 |
| *元件* | 工具、多模態、AgentTools |
| *垂直領域* | 金融服務 |

### 代理程式架構

此圖顯示了用於實作此工作流程的代理程式和工具的詳細架構。
![FOMC 研究代理程式架構](<fomc-research.svg>)

### 主要功能

##### 代理程式
* **root_agent:** 代理程式工作流程的進入點。協調其他代理程式的活動。
* **research_agent:** 協調個別研究元件的擷取。
* **analysis_agent:** 接收 `research_agent` 的輸出並產生分析報告。
* **retrieve_meeting_data_agent:** 從網路上擷取 FOMC 會議資料。
* **extract_page_data_agent:** 從 HTML 頁面擷取特定資料。
* **summarize_meeting_agent:** 讀取會議記錄並產生摘要。

##### 工具
* **fetch_page_tool**: 封裝用於擷取網頁的 HTTP 請求。
* **store_state_tool**: 將特定資訊儲存在 ToolContext 中。
* **analyze_video_tool**: 處理和分析 YouTube 影片。
* **compute_probability_tool**: 從聯邦基金期貨定價計算利率變動的機率。
* **compare_statements**: 比較目前和先前的 FOMC 聲明。
* **fetch_transcript**: 擷取 FOMC 會議記錄。

##### 回呼函式
* **rate_limit_callback**: 實作請求速率限制，以最小化 `429: Resource Exhausted` 錯誤。

## 設定與安裝
1.  **先決條件：**

    **Google Cloud SDK 和 GCP 專案：**

    對於 BigQuery 設定和 Agent Engine 部署步驟，您將需要一個 Google Cloud 專案。建立專案後，[安裝 Google Cloud SDK](https://cloud.google.com/sdk/docs/install)。然後執行以下指令以使用您的專案進行驗證：
    ```bash
    gcloud auth login
    ```
    您還需要啟用某些 API。執行以下指令以啟用所需的 API：
    ```bash
    gcloud services enable aiplatform.googleapis.com
    gcloud services enable bigquery.googleapis.com
    ```

2.  **安裝：**

    複製此儲存庫並切換到儲存庫目錄：
    ```
    git clone https://github.com/google/adk-samples.git
    cd adk-samples/agents/fomc-research
    ```

    安裝 [Poetry](https://python-poetry.org)。

    安裝 FOMC 研究代理程式的需求：
    ```bash
    poetry install
    ```

    這也會安裝已發行的 'google-adk' 版本，即 Google Agent Development Kit。

3.  **設定：**

    **環境：**

    儲存庫中包含一個 `.env-example` 檔案。使用適合您專案的值更新此檔案，並將其另存為 `.env`。此檔案中的值將讀取到您應用程式的環境中。

    建立 `.env` 檔案後，如果您使用的是 `bash` shell，請執行以下指令將 `.env` 檔案中的變數匯出到您的本機 shell 環境中：
    ```bash
    set -o allexport
    . .env
    set +o allexport
    ```
    如果您未使用 `bash`，則可能需要手動匯出變數。

    **BigQuery 設定：**

    您需要建立一個包含聯邦基金期貨定價資料的 BigQuery 表格。

    FOMC 研究代理程式儲存庫包含一個範例資料檔案 (`sample_timeseries_data.csv`)，其中包含涵蓋 2025 年 1 月 29 日和 3 月 19 日 FOMC 會議的資料。如果您想針對其他 FOMC 會議執行代理程式，則需要取得額外的資料。

    若要將此資料檔案安裝到您專案中的 BigQuery 表格，請在 `fomc-research/deployment` 目錄中執行以下指令：
    ```bash
    python bigquery_setup.py --project_id=$GOOGLE_CLOUD_PROJECT \
        --dataset_id=$GOOGLE_CLOUD_BQ_DATASET \
        --location=$GOOGLE_CLOUD_LOCATION \
        --data_file=sample_timeseries_data.csv
    ```

## 執行代理程式

**使用 ADK 命令列：**

從 `fomc-research` 目錄執行此指令：
```bash
adk run fomc_research
```
初始輸出將包含一個可用於追蹤代理程式記錄檔的指令。該指令將類似於：
```bash
tail -F /tmp/agents_log/agent.latest.log
```

**使用 ADK 開發 UI：**

從 `fomc-research` 目錄執行此指令：
```bash
adk web .
```
它將顯示示範 UI 的 URL。將您的瀏覽器指向該 URL。

UI 最初將是空白的。在左上角的下拉式選單中，選擇 `fomc_research` 以載入代理程式。

代理程式的記錄將在執行時即時顯示在主控台上。但是，如果您想儲存互動記錄並同時即時追蹤互動，請使用以下指令：

```bash
adk web . > fomc_research_log.txt 2>&amp;1 &amp;
tail -f fomc_research_log.txt
```

### 範例互動

輸入「Hello. What can you do for me?」開始互動。在第一個提示後，輸入日期：「2025-01-29」。

互動將類似於：
```
$ adk run .
Log setup complete: /tmp/agents_log/agent.20250405_140937.log
To access latest log: tail -F /tmp/agents_log/agent.latest.log
Running agent root_agent, type exit to exit.
user: Hello. What can you do for me?
[root_agent]: 我可以協助您分析過去的聯邦公開市場委員會 (FOMC) 會議，並提供您詳盡的分析報告。首先，請提供您想分析的會議日期。如果您已經提供，請確認日期。我需要 ISO 格式 (YYYY-MM-DD) 的日期。

user: 2025-01-29
[analysis_agent]: 根據現有資訊，以下是 2025 年 1 月 29 日 FOMC 會議的摘要和分析：
...
```
如果代理程式在完成分析之前停止，請嘗試要求它繼續。

## 在 Vertex AI Agent Engine 上部署

若要將代理程式部署到 Google Agent Engine，請先遵循[這些步驟](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/set-up)來設定您的 Google Cloud 專案以用於 Agent Engine。

您還需要授予 BigQuery 使用者和 BigQuery 資料檢視者權限給 Reasoning Engine Service Agent。執行以下指令以授予所需的權限：
```bash
export RE_SA="service-${GOOGLE_CLOUD_PROJECT_NUMBER}@gcp-sa-aiplatform-re.iam.gserviceaccount.com"
gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} \
    --member="serviceAccount:${RE_SA}" \
    --condition=None \
    --role="roles/bigquery.user"
gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} \
    --member="serviceAccount:${RE_SA}" \
    --condition=None \
    --role="roles/bigquery.dataViewer"
```
接下來，您需要為您的代理程式建立一個 `.whl` 檔案。從 `fomc-research` 目錄執行此指令：
```bash
poetry build --format=wheel --output=deployment
```
這將在 `deployment` 目錄中建立一個名為 `fomc_research-0.1-py3-none-any.whl` 的檔案。

然後執行以下指令：
```bash
cd deployment
python3 deploy.py --create
```
當此指令傳回時，如果成功，它將列印一個 AgentEngine 資源名稱，類似於：
```
projects/************/locations/us-central1/reasoningEngines/7737333693403889664
```
最後一串數字是 AgentEngine 資源 ID。

成功部署代理程式後，您可以使用 `deployment` 目錄中的 `test_deployment.py` 指令碼與其互動。將代理程式的資源 ID 儲存在環境變數中，然後執行以下指令：
```bash
export RESOURCE_ID=...
export USER_ID=<any string>
python test_deployment.py --resource_id=$RESOURCE_ID --user_id=$USER_ID
```
工作階段將類似於：
```
Found agent with resource ID: ...
Created session for user ID: ...
Type 'quit' to exit.
Input: Hello. What can you do for me?
Response: 我可以建立 FOMC 會議的分析報告。首先，請提供您想分析的會議日期。我需要 YYYY-MM-DD 格式的日期。

Input: 2025-01-29
Response: 我已儲存您提供的日期。現在我將擷取會議資料。
...
```
請注意，這*不是*一個功能齊全、可用於生產環境的 CLI；它僅用於展示如何使用 Agent Engine API 與已部署的代理程式互動。

`test_deploy.py` 指令碼的主要部分大致如下：

```python
from vertexai import agent_engines
remote_agent = vertexai.agent_engines.get(RESOURCE_ID)
session = remote_agent.create_session(user_id=USER_ID)
while True:
    user_input = input("Input: ")
    if user_input == "quit":
      break

    for event in remote_agent.stream_query(
        user_id=USER_ID,
        session_id=session["id"],
        message=user_input,
    ):
        parts = event["content"]["parts"]
        for part in parts:
            if "text" in part:
                text_part = part["text"]
                print(f"Response: {text_part}")
```

若要刪除代理程式，請執行以下指令（使用先前傳回的資源 ID）：
```bash
python3 deployment/deploy.py --delete --resource_id=$RESOURCE_ID
```

## 疑難排解

### "Malformed function call" (函式呼叫格式錯誤)

代理程式偶爾會傳回「Malformed function call」錯誤。這是 Gemini 模型錯誤，應在未來的模型版本中解決。只需重新啟動 UI，代理程式就會重設。

### 代理程式在工作流程中停止

有時代理程式會在完成其中一個中間步驟後在工作流程中停止。發生這種情況時，通常只需告訴代理程式繼續，或給予另一個指令以繼續其操作即可。