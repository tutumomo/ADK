# 使用多個 Agent 進行數據科學

## 概觀

本專案展示了一個專為複雜數據分析而設計的多 Agent 系統。它整合了數個專門的 Agent 來處理數據流程的不同面向，從數據擷取到進階分析和機器學習。此系統旨在與 BigQuery 互動、執行複雜的數據操作、產生數據視覺化圖表，並使用 BigQuery ML (BQML) 執行機器學習任務。Agent 可以產生文字回應以及視覺化圖表，包括用於數據分析和探索的圖表。

## Agent 詳細資訊
數據科學多 Agent 的主要功能包括：

| 功能 | 描述 |
| --- | --- |
| **互動類型：** | 對話式 |
| **複雜度：**  | 進階 |
| **Agent 類型：**  | 多 Agent |
| **元件：**  | 工具、AgentTools、會話記憶體、RAG |
| **垂直領域：**  | 所有（適用於需要進階數據分析的各行各業） |


### 架構
![數據科學架構](data-science-architecture.png)


### 主要功能

*   **多 Agent 架構：** 利用一個頂層 Agent 來協調子 Agent，每個子 Agent 專精於特定任務。
*   **資料庫互動 (NL2SQL)：** 採用資料庫 Agent，使用自然語言查詢與 BigQuery 互動，並將其翻譯成 SQL。
*   **數據科學分析 (NL2Py)：** 包含一個數據科學 Agent，根據自然語言指令使用 Python 執行數據分析和視覺化。
*   **機器學習 (BQML)：** 具有一個 BQML Agent，利用 BigQuery ML 進行機器學習模型的訓練和評估。
*   **程式碼解釋器整合：** 支援在 Vertex AI 中使用程式碼解釋器擴充功能來執行 Python 程式碼，從而實現複雜的數據分析和操作。
*   **ADK Web GUI：** 提供一個使用者友善的 GUI 介面，用於與 Agent 互動。
*   **可測試性：** 包含一個全面的測試套件，以確保 Agent 的可靠性。



## 設定與安裝

### 先決條件

*   **Google Cloud 帳戶：** 您需要一個已啟用 BigQuery 的 Google Cloud 帳戶。
*   **Python 3.9+：** 確保您已安裝 Python 3.9 或更新版本。
*   **Poetry：** 依照 Poetry 官方網站上的說明安裝 Poetry：[https://python-poetry.org/docs/](https://python-poetry.org/docs/)
*   **Git：** 確保您已安裝 git。如果沒有，您可以從 [https://git-scm.com/](https://git-scm.com/) 下載並依照[安裝指南](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)進行安裝。



### 使用 Poetry 設定專案

1.  **複製儲存庫：**

    ```bash
    git clone https://github.com/google/adk-samples.git
    cd google-adk-samples/agents/data-science
    ```

2.  **使用 Poetry 安裝依賴項：**

    ```bash
    poetry install
    ```

    此命令會讀取 `pyproject.toml` 檔案，並將所有必要的依賴項安裝到由 Poetry 管理的虛擬環境中。

3.  **啟動 Poetry Shell：**

    ```bash
    poetry env activate
    ```

    這會啟動虛擬環境，讓您可以在專案的環境中執行命令。
    確保環境已啟動。如果沒有，您也可以透過以下方式啟動：

     ```bash
    source .venv/bin/activate
    ```

4.  **設定環境變數：**
    將檔案 ".env-example" 重新命名為 ".env"
    填寫以下值：

    ```bash
    # 選擇模型後端：0 -> ML Dev，1 -> Vertex
    GOOGLE_GENAI_USE_VERTEXAI=1

    # ML Dev 後端設定。如果使用 ML Dev 後端，請填寫。
    GOOGLE_API_KEY='YOUR_VALUE_HERE'

    # Vertex 後端設定
    GOOGLE_CLOUD_PROJECT='YOUR_VALUE_HERE'
    GOOGLE_CLOUD_LOCATION='YOUR_VALUE_HERE'
    ```

    依照以下步驟設定其餘的環境變數。

5.  **BigQuery 設定：**
    這些步驟會將此儲存庫中提供的範例數據載入 BigQuery。
    在我們的範例使用案例中，我們正在處理來自 Kaggle 的 Forecasting Sticker Sales 數據：

    _Walter Reade and Elizabeth Park. Forecasting Sticker Sales. https://kaggle.com/competitions/playground-series-s5e1, 2025. Kaggle._

    *   首先，在 `.env` 檔案中設定 BigQuery 專案 ID。這可以與您用於 `GOOGLE_CLOUD_PROJECT` 的 GCP 專案相同，
        但您也可以使用其他 BigQuery 專案，只要您具有該專案的存取權限即可。
        如果您有現有的 BigQuery 資料表想要連接，請同時在 `.env` 檔案中指定 `BQ_DATASET_ID`。
        如果您想使用範例數據，請確保將 `BQ_DATASET_ID` 保留為 `'forecasting_sticker_sales'`。

        或者，您可以從終端機設定變數：

        ```bash
        export BQ_PROJECT_ID='YOUR-BQ-PROJECT-ID'
        export BQ_DATASET_ID='YOUR-DATASET-ID' # 如果使用範例數據，請保留為 'forecasting_sticker_sales'
        ```

        如果您使用自己的數據，可以跳過上傳步驟。我們建議不要將任何生產關鍵數據集添加到此範例 Agent 中。
        如果您想使用範例數據，請繼續下一步。

    *   您會在 'data-science/data_science/utils/data/' 中找到數據集。
        確保您仍在工作目錄 (`agents/data-science`) 中。若要將測試和訓練資料表載入 BigQuery，請執行以下命令：
        ```bash
        python3 data_science/utils/create_bq_table.py
        ```


6.  **BQML 設定：**
    BQML Agent 使用 Vertex AI RAG Engine 來查詢完整的 BigQuery ML 參考指南。

    在執行設定之前，請確保您的專案 ID 已新增到 .env 檔案中：`"GOOGLE_CLOUD_PROJECT"`。
    將語料庫名稱保留為空值於 .env 檔案中：`BQML_RAG_CORPUS_NAME = ''`。語料庫名稱將在建立後自動新增。

    若要為您的專案設定 RAG 語料庫，請在
    `data-science/data_science/utils/reference_guide_RAG.py` 中執行 `create_RAG_corpus()` 和 `ingest_files()` 方法，方法是從工作目錄執行以下命令：

    ```bash
    python3 data_science/utils/reference_guide_RAG.py
    ```


7.  **其他環境變數：**

    *   `CODE_INTERPRETER_EXTENSION_NAME`：（選用）Vertex AI 中
        預先存在的程式碼解釋器擴充功能的完整資源名稱。如果未提供，
        將會建立一個新的擴充功能。（例如，
        `projects/<YOUR_PROJECT_ID>/locations/<YOUR_LOCATION>/extensions/<YOUR_EXTENSION_ID>`）。
        檢查日誌/終端機以取得新建立的程式碼解釋器
        擴充功能的 ID，並在您的環境變數中提供該值，以避免
        建立多個擴充功能。

    從終端機：

    ```bash
    export CODE_INTERPRETER_EXTENSION_NAME='projects/<YOUR_PROJECT_ID>/locations/us-central1/extensions/<YOUR_EXTENSION_ID>'
    ```

## 執行 Agent

您可以使用終端機中的 ADK 命令來執行 Agent。
從工作目錄：

1.  在 CLI 中執行 Agent：

    ```bash
    poetry run adk run data_science
    ```

2.  使用 ADK Web UI 執行 Agent：
    ```bash
    poetry run adk web
    ```
    從下拉式選單中選取 data_science



### Agent 互動範例

以下是一個使用者如何與數據科學多 Agent 系統互動的快速範例：

> ´**使用者：** 嗨，您能存取哪些數據？

> **Agent：** 我可以存取兩個資料表：`train` 和 `test`。兩個資料表都包含貼紙銷售數據，具有以下欄位：`id`、`date`、`country`、`store`、`product` 和 `num_sold`。

> **使用者：** 我需要 train 資料表的更多詳細資訊。有哪些國家？有多少家商店？

> **Agent：** 結果：train 資料表包含來自加拿大、芬蘭、義大利、肯亞、挪威和新加坡的數據。這些國家各有 3 家不同的商店。

>說明：資料庫 Agent 對 train 資料表執行了 SQL 查詢，以找出不同的國家以及每個國家內不同商店的數量。查詢按國家分組結果，並計算了不同的商店值。

> **使用者：** 請產生一個顯示每個國家總銷售額的圖表。

> **Agent：** 結果：已產生一個長條圖，顯示每個國家的總銷售額。X 軸代表國家，Y 軸代表總銷售額。

> 說明：
> 1. 首先呼叫資料庫 Agent，從 train 資料表中擷取每個國家的總銷售額。
> 2. 然後呼叫數據科學 Agent，產生一個視覺化結果的長條圖。圖表在 X 軸上顯示每個國家，在 Y 軸上顯示其對應的總銷售額。

> **使用者：** 我可以在 BQML 中訓練哪些類型的預測模型？

> **Agent：** 您可以在 BQML 中訓練多種類型的預測模型，包括 ARIMA、指數平滑法和時間融合轉換器 (TFT) 模型。您想繼續訓練預測模型嗎？

> **使用者：** 是

> **Agent：** 好的，在繼續之前，讓我們確認 BQML 的專案和數據集 ID。我們將使用 `PROJECT_ID` 專案和 `forecasting_sticker_sales` 數據集。這樣對嗎？

> **使用者：** 是

> **Agent：** BQML 支援 `ARIMA_PLUS`、`ARIMA_PLUS_XREG`。

>若要繼續，我需要知道您想使用哪個模型。我還需要知道以下資訊：

>*   提供時間點的欄位名稱（例如，'date'）。
>*   包含要預測的數據的欄位名稱（例如，'num_sold'）。
>*   您想使用單一查詢來擬合和預測多個時間序列嗎？如果是，ID 欄位是什麼？（例如，`country`、`store`、`product`）


## 執行評估


評估測試以整體方式評估 Agent 的整體效能和能力。

**執行評估測試：**

    ```bash
    poetry run pytest eval
    ```


- 此命令會執行 `eval/` 目錄中的所有測試檔案。
- `poetry run` 確保 pytest 在專案的虛擬環境中執行。



## 執行測試

測試評估 Agent 的整體可執行性。

**測試類別：**

*   **整合測試：** 這些測試驗證 Agent 是否能正確地彼此互動以及與 BigQuery 等外部服務互動。它們確保根 Agent 可以將任務委派給適當的子 Agent，並且子 Agent 可以執行其預期任務。
*   **子 Agent 功能測試：** 這些測試著重於每個子 Agent（例如，資料庫 Agent、BQML Agent）的特定能力。它們確保每個子 Agent 都能執行其預期任務，例如執行 SQL 查詢或訓練 BQML 模型。
*   **環境查詢測試：** 這些測試驗證 Agent 是否能處理基於環境的查詢。

**執行測試：**

    ```bash
    poetry run pytest tests
    ```

- 此命令會執行 `tests/` 目錄中的所有測試檔案。
- `poetry run` 確保 pytest 在專案的虛擬環境中執行。



## 在 Vertex AI Agent Engine 上部署

若要將 Agent 部署到 Google Agent Engine，請先依照
[這些步驟](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/set-up)
設定您的 Google Cloud 專案以使用 Agent Engine。

您還需要授予 BigQuery 使用者和 BigQuery 資料檢視者權限給
Reasoning Engine Service Agent。執行以下命令以授予所需的
權限：

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

接下來，您需要為您的 Agent 建立一個 `.whl` 檔案。從 `data-science`
目錄執行此命令：

```bash
poetry build --format=wheel --output=deployment
```

這會在 `deployment` 目錄中建立一個名為 `data_science-0.1-py3-none-any.whl` 的檔案。

然後執行以下命令。這會在您的 GCP 專案中建立一個暫存儲存桶，並將 Agent 部署到 Vertex AI Agent Engine：

```bash
python3 deployment/deploy.py --create
```

當此命令傳回時，如果成功，它將列印一個 AgentEngine 資源
名稱，如下所示：
```
projects/************/locations/us-central1/reasoningEngines/7737333693403889664
```
最後一串數字是 AgentEngine 資源 ID。

成功部署 Agent 後，您可以使用 `deployment` 目錄中的
`test_deployment.py` 指令碼與其互動。將 Agent 的資源 ID 儲存在
環境變數中，並執行以下命令：

```bash
export RESOURCE_ID=...
export USER_ID=<any string>
python test_deployment.py --resource_id=$RESOURCE_ID --user_id=$USER_ID
```

會話將如下所示：
```
Found agent with resource ID: ...
Created session for user ID: ...
Type 'quit' to exit.
Input: Hello. What data do you have?
Response: I have access to the train and test tables inside the forecasting_sticker_sales dataset.
...
```

請注意，這*不是*一個功能齊全、可用於生產環境的 CLI；它僅用於
展示如何使用 Agent Engine API 與已部署的 Agent 互動。

`test_deployment.py` 指令碼的主要部分大致如下：

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

若要刪除 Agent，請執行以下命令（使用先前傳回的資源 ID）：
```bash
python3 deployment/deploy.py --delete --resource_id=RESOURCE_ID
```



## 優化與調整提示

*   **提示工程：** 優化 `root_agent`、`bqml_agent`、`db_agent`
    和 `ds_agent` 的提示，以提高準確性並更有效地引導 Agent。
    嘗試不同的措辭和詳細程度。
*   **擴充：** 使用您自己的 AgentTools 或 sub_agents 來擴充多 Agent 系統。
    您可以透過在 `agents/data-science/data_science/agent.py` 內的根 Agent 中
    新增額外的工具和子 Agent 來實現。
*   **部分匯入：** 如果您只需要多 Agent 系統中的某些功能，
    例如只需要數據 Agent，您可以將 data_agent 作為 AgentTool 匯入您自己的根 Agent 中。
*   **模型選擇：** 為頂層 Agent 和子 Agent 嘗試不同的語言模型，
    以找出最適合您的數據和查詢的效能。


## 疑難排解

*   如果您在執行 Agent 時遇到 `500 Internal Server Errors`，只需重新執行您最後的命令即可。
    這應該可以解決問題。
*   如果您遇到程式碼解釋器的問題，請檢閱日誌以
    了解錯誤。如果您直接與程式碼解釋器擴充功能互動
    而不是透過 Agent 的輔助函式，請確保您對
    檔案/圖片使用 base-64 編碼。
*   如果您在產生的 SQL 中看到錯誤，請嘗試以下方法：
    - 在您的資料表和欄位中包含清晰的描述有助於提高效能
    - 如果您的資料庫很大，請嘗試透過將您的資料表結構詳細資訊儲存在向量儲存庫中來設定 RAG 管線以進行結構連結