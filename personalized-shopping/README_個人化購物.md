# 個人化購物

## 代理程式概觀

此代理程式範例可在特定品牌、商家或線上市場的生態系統內，有效率地提供量身打造的產品推薦。它透過使用目標資料並提供相關建議，提升其自身情境下的購物體驗。

### 代理程式詳細資訊

個人化購物代理程式具備以下能力：

*   瀏覽特定網站以收集產品資訊並了解可用選項。
*   使用應用於特定目錄的文字和圖片搜尋來識別合適的產品。
*   在定義的品牌或市場範圍內比較產品功能。
*   根據使用者行為和個人資料推薦產品。

代理程式的預設設定可讓您模擬與專注型購物者的互動。它展示了代理程式如何在特定的零售環境中導覽。

| <div align="center">功能</div> | <div align="center">說明</div> |
| --- | --- |
| <div align="center">**互動類型**</div> | <div align="center">對話式</div> |
| <div align="center">**複雜度**</div>  | <div align="center">簡單</div> |
| <div align="center">**代理程式類型**</div>  | <div align="center">單一代理程式</div> |
| <div align="center">**元件**</div>  | <div align="center">網路環境：存取預先索引的產品網站</div> |
|  | <div align="center">搜尋工具 (SearchTool) (用於擷取相關產品資訊)</div> |
|  | <div align="center">點擊工具 (ClickTool) (用於導覽網站)</div> |
|  | <div align="center">對話記憶體</div> |
| <div align="center">**垂直領域**</div>  | <div align="center">電子商務</div> |


### 架構
![個人化購物代理程式架構](ps_architecture.png)

### 主要功能

個人化購物代理程式的主要功能包括：
*   **環境：** 代理程式可以在包含 118 萬種產品的電子商務網路環境中互動。
*   **記憶體：** 代理程式在其內容視窗中維護一個包含所有先前對話資訊的對話記憶體。
*   **工具：**

    _搜尋_：代理程式可以存取搜尋擷取引擎，在其中執行相關產品的關鍵字搜尋。

    _點擊_：代理程式可以存取產品網站，並透過點擊按鈕來導覽網站。
*   **評估：**
    代理程式使用 `tool_trajectory_avg_score` 和 `response_match_score` 來衡量使用者滿意度。

    評估程式碼位於 `eval/test_eval.py`。

    工具的單元測試位於 `tests/test_tools.py`。


## 設定與安裝

重要提示：
* 您應使用 [poetry](https://python-poetry.org/docs/) 來管理 Python 的相依性套件和打包。
* 您的儲存庫應包含一個 .env 範例檔案，說明使用了哪些環境變數以及如何啟用 .env。

1.  **先決條件：**

*   首先，請先 _複製此儲存庫_，然後使用下方的 poetry 指令安裝必要的套件。

    ```bash
    cd ~
    python3 -m venv myenv
    source ~/myenv/bin/activate
    pip install poetry
    ```

*   然後進入專案資料夾，並執行以下指令：

    ```bash
    cd agents/personalized-shopping
    poetry install
    ```

2.  **安裝：**

*   若要執行代理程式，請先下載包含產品資訊的 JSON 檔案，這些檔案是初始化代理程式將互動的網路環境所必需的。

    ```bash
    cd personalized_shopping/shared_libraries
    mkdir data
    cd data

    # 下載 items_shuffle_1000 (4.5MB)
    gdown https://drive.google.com/uc?id=1EgHdxQ_YxqIQlvvq5iKlCrkEKR6-j0Ib;

    # 下載 items_ins_v2_1000 (147KB)
    gdown https://drive.google.com/uc?id=1IduG0xl544V_A_jv3tHXC0kyFi7PnyBu;

    # 下載 items_shuffle (5.1GB)
    gdown https://drive.google.com/uc?id=1A2whVgOO0euk5O13n2iYDM0bQRkkRduB;

    # 下載 items_ins_v2 (178MB)
    gdown https://drive.google.com/uc?id=1s2j6NgHljiZzQNL3veZaAiyW_qDEgBNi;

    # 下載 items_human_ins (4.9MB)
    gdown https://drive.google.com/uc?id=14Kb5SPBk_jfdLZ_CDBNitW98QLDlKR5O
    ```

*   接著，您需要為產品資料建立索引，以便搜尋引擎可以使用它們：

    ```bash
    # 將 items.json 轉換為 => 所需的文件格式
    cd ../search_engine
    mkdir -p resources_100 resources_1k resources_10k resources_50k
    python convert_product_file_format.py

    # 為產品建立索引
    mkdir -p indexes
    bash run_indexing.sh
    cd ../../
    ```
3.  **設定：**

*   使用您的雲端專案名稱和區域更新 `.env.example` 檔案，然後將其重新命名為 `.env`。

*   驗證您的 GCloud 帳戶。

    ```bash
    gcloud auth application-default login
    ```

## 執行代理程式

- **選項 1**：您可以使用 CLI 與代理程式對話：

    ```bash
    adk run personalized_shopping
    ```

- **選項 2**：您可以在網頁介面上執行代理程式。這將在您的機器上啟動一個網頁伺服器。您可以前往螢幕上顯示的 URL，並在聊天機器人介面中與代理程式互動。

    ```bash
    cd personalized-shopping
    adk web
    ```
    請從螢幕左上角的下拉式清單中選取 `personalized_shopping` 選項。現在您可以開始與代理程式對話了！


> **注意**：第一次執行可能需要一些時間，因為系統會將大約 50,000 個產品項目載入到搜尋引擎的網路環境中。:)

### 互動範例

使用者可以使用文字搜尋和圖片搜尋來尋找產品推薦。以下是使用者可能與代理程式互動的兩個快速範例。

____________

#### 範例 1：文字搜尋

*   工作階段檔案：[text_search_floral_dress.session.json](tests/example_interactions/text_search_floral_dress.session.md)

#### 範例 2：圖片搜尋

*   工作階段檔案：[image_search_denim_skirt.session.json](tests/example_interactions/text_search_floral_dress.session.md) (此工作階段的輸入圖片檔案為 [example_product.png](tests/example_interactions/example_product.png))

## 執行評估

評估會根據 evalset 中定義的任務來評量代理程式的效能。evalset 中的每個範例都包含一個查詢、預期的工具使用方式和一個參考答案。判斷標準在 `test_config.json` 中指定。

代理程式的評估可以從 `personalized-shopping` 目錄使用 `pytest` 模組執行：

```bash
python3 -m pytest eval
```

您可以將您的資料集新增到 `eval/eval_data` 資料夾中，以新增更多評估提示。

若要執行工具的單元測試，您可以從 `personalized-shopping` 目錄執行以下指令：

```bash
python3 -m pytest tests
```

## 部署

*   個人化購物代理程式範例可以部署到 Vertex AI Agent Engine。為了繼承代理程式的所有相依性套件，您可以建置代理程式的 wheel 檔案並執行部署。

1.  **建置個人化購物代理程式 WHL 檔案**

    ```bash
    cd agents/personalized-shopping
    poetry build --format=wheel --output=deployment
    ```

1.  **將代理程式部署到 Agents Engine**

    ```bash
    cd agents/personalized-shopping/deployment
    python3 deploy.py
    ```

    > **注意**：此過程可能需要超過 10 分鐘才能完成，請耐心等候。

部署完成後，將會印出類似這樣的一行：

```
Created remote agent: projects/<PROJECT_NUMBER>/locations/<PROJECT_LOCATION>/reasoningEngines/<AGENT_ENGINE_ID>
```

您可以使用 Python 以程式設計方式與已部署的代理程式互動：

```python
import dotenv
dotenv.load_dotenv()  # 如果您已匯出環境變數，則可略過。
from vertexai import agent_engines

agent_engine_id = "AGENT_ENGINE_ID" # 請記得在此更新 ID。
user_input = "你好，可以幫我找一件夏天的洋裝嗎？我想要飄逸的花卉圖案。"

agent_engine = agent_engines.get(agent_engine_id)
session = agent_engine.create_session(user_id="new_user")
for event in agent_engine.stream_query(
    user_id=session["user_id"], session_id=session["id"], message=user_input
):
    for part in event["content"]["parts"]:
        print(part["text"])
```

若要刪除已部署的代理程式，您可以執行以下指令：

```bash
python3 deployment/deploy.py --delete --resource_id=${AGENT_ENGINE_ID}
```

## 自訂

此代理程式範例使用來自 [princeton-nlp/WebShop](https://github.com/princeton-nlp/WebShop) 的 webshop 環境，其中包含 118 萬個真實世界的產品和 12,087 個群眾外包的文字說明。

預設情況下，代理程式僅將 50,000 個產品載入環境中，以防止記憶體不足 (OOM) 問題。您可以透過修改 [init_env.py](personalized_shopping/shared_libraries/init_env.py) 中的 `num_product_items` 參數來調整此設定。

若要進行自訂，您可以新增自己的產品資料，並將註釋放在 `items_human_ins.json`、`items_ins_v2.json` 和 `items_shuffle.json` 中，然後輕鬆啟動代理程式範例。

## 疑難排解

* **問題 1：** 我在代理程式設定期間遇到 `gdown` 的問題。該怎麼辦？
* **答案 1：** 您可以從個別的 Google 雲端硬碟連結手動下載檔案，並將它們放在 `personalized-shopping/personalized_shopping/shared_libraries/data` 資料夾中。

## 致謝
我們感謝 [princeton-nlp/WebShop](https://github.com/princeton-nlp/WebShop) 的開發人員提供模擬環境。此代理程式整合了他們專案中經過修改的程式碼。