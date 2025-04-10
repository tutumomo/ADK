# 品牌搜尋優化 - 用於搜尋優化的網頁瀏覽器代理程式

## 概觀

此代理程式旨在增強零售網站的產品資料。它會根據產品資料（例如標題、描述和屬性）產生關鍵字。然後，它會造訪網站、進行搜尋並分析排名靠前的結果，以提供豐富產品標題的建議。這有助於透過識別產品資料中的差距來解決「空值和低回收率」或「零結果」搜尋等問題。此代理程式可以擴展以支援豐富描述和屬性。它使用的主要工具是：電腦使用和 BigQuery 資料連線。

## 代理程式詳細資訊

此代理程式展示了具有工具呼叫和網頁爬取的 Multi Agent 設定。

| 屬性 | 詳細資訊 |
|---|---|
|   互動類型 |   工作流程 |
|   複雜度 |   進階 |
|   代理程式類型 |   Multi Agent |
|   Multi Agent 設計模式： |   路由器代理程式 |
|   元件 |   BigQuery 連線、電腦使用、工具、評估 |
|   垂直領域 |   零售 |

### 代理程式架構

![品牌搜尋優化](./brand_search_optimization.png)

### 主要功能

* **工具：**

  * `function_calling`：根據使用者提供的品牌從產品目錄（即 BigQuery 表格）取得資料。它以品牌字串作為輸入，並傳回資料庫記錄清單。

  * `load_artifacts_tool`：將網頁原始碼資料載入為成品，以分析元件以採取動作，例如按一下搜尋按鈕。

  * `網站爬取`：透過數個個別工具實現，例如 `go_to_url`、`take_screenshot`、`find_element_with_text`、`click_element_with_text`、`enter_text_into_element`、`scroll_down_screen`、`get_page_source`、`analyze_webpage_and_determine_action`

* **評估：** 此代理程式使用 ADK 提供的 OOTB 評估，可以使用 `sh deployment/eval.sh` 指令碼執行。

## 設定與安裝

1. **先決條件：**
    * Python 3.11+
    * Poetry
        * 用於相依性管理和封裝。請依照官方 [Poetry 網站](https://python-poetry.org/docs/) 上的說明進行安裝。
    * Google Cloud Platform 上的專案
    * 從[這裡](https://aistudio.google.com)取得您的 API 金鑰。（如果您想使用 Vertex AI 中的 Gemini，則不需要）

2. **設定：**
    * 環境檔案設定
        * 複製範例環境檔案 `cp env.example .env`
        * 設定 `DISABLE_WEB_DRIVER=1`
        * 在 `.env` 檔案中為下列變數新增值
            * `GOOGLE_CLOUD_PROJECT=<您的專案>`
            * `GOOGLE_CLOUD_LOCATION=<您的位置>`

    * **API 金鑰：**
        * 您的 API 金鑰應新增至 `.env` 中的 `GOOGLE_API_KEY` 變數下
        * 您不需要同時設定 Google API 金鑰和 Vertex AI。任一設定皆可運作。
    * **BigQuery 設定**
        * BigQuery DATASET_ID 應位於 `.env` 中的 `DATASET_ID` 下
        * BigQuery TABLE_ID 應位於 `.env` 中的 `TABLE_ID` 下
        * BigQuery 表格設定可以透過自動執行下列 `sh deployment/run.sh` 或手動依照「BigQuery 設定」區段中的步驟完成。

    * **其他設定：**
        * 您可以透過變更 `.env` 下的 `MODEL` 來變更 Gemini 模型
        * 將 `DISABLE_WEB_DRIVER` 設定為 `1` 時，將啟用您執行單元測試。請參閱下方的「單元測試」區段以取得詳細資訊。**注意** 在不進行測試時，預設將此旗標保持為 0。

3.  **使用您的 Google Cloud 帳戶進行驗證：**
    ```bash
    gcloud auth application-default login
    ```

4. **安裝：**

    * 使用 `deployment/run.sh` 安裝相依性並填入資料庫

        `````bash
        # 複製此儲存庫。
        git clone https://github.com/google/adk-samples.git
        cd agents/brand-search-optimization

        # 執行此指令碼
        # 1. 建立並啟用新的虛擬環境
        # 2. 安裝 Python 套件
        # 3. 使用 `.env` 檔案中設定的變數填入 BigQuery 資料
        sh deployment/run.sh
        `````

    * 設定 `DISABLE_WEB_DRIVER=0`

## 執行代理程式

您必須執行 `adk run brand_search_optimization` 才能讓代理程式執行。

您也可以使用以下指令執行 Web 應用程式

您也可以使用 `adk web` 執行 Web 應用程式。

指令 `adk web` 將在您的機器上啟動 Web 伺服器並列印 URL。您可以開啟 URL 並在聊天機器人介面中與代理程式互動。UI 最初是空白的。

從下拉式功能表中選取「brand-search-optimization」。

> **注意** 這應該會透過 Web 驅動程式開啟一個新的 Chrome 視窗。如果沒有，請確保 `.env` 檔案中的 `DISABLE_WEB_DRIVER=0`。

### 品牌名稱

* 如果您執行了 `deployment/run.sh` 指令碼。代理程式將預先設定為品牌 `BSOAgentTestBrand`。當代理程式要求品牌名稱時，請提供 `BSOAgentTestBrand` 作為您的品牌名稱。
* 對於自訂資料，請修改品牌名稱。
* 當您提供品牌名稱時，代理程式流程會觸發。

> **注意**
>
> * 請勿關閉代理程式開啟的額外 Chrome 視窗。
> * 在代理程式提供關鍵字清單後，要求代理程式搜尋網站。例如：「您可以搜尋網站嗎？」、「您可以在網站上搜尋關鍵字嗎？」、「幫我在網站上搜尋關鍵字」等。
> * 造訪 Google Shopping 網站時，您需要在首次執行時完成驗證碼。完成驗證碼後，代理程式應在後續執行中執行。

### 範例互動

提供了一個範例工作階段，以說明品牌搜尋優化器如何針對品牌 BSOAgentTestBrand 與 Google Shopping 搭配運作 - [`example_interaction.md`](tests/example_interaction.md)

此檔案包含使用者與各種代理程式和工具之間的完整對話記錄，從關鍵字尋找到前 3 個搜尋結果標題的完整比較報告。

> **免責聲明** 此範例使用 Google Shopping 網站進行示範，但您有責任確保遵守該網站的服務條款。

## 評估代理程式

這會使用 ADK 的評估元件，以 `eval/data/` 內的 evalset 和 `eval/data/test_config.json` 中定義的設定來評估品牌搜尋優化代理程式。

您必須位於 `brand-search-optimization` 目錄內，然後執行

```bash
sh deployment/eval.sh
```

## 單元測試

依照下列步驟使用 `pytest` 執行單元測試

1. 在 `.env` 中修改此項 `DISABLE_WEB_DRIVER=1`

2. 執行 `sh deployment/test.sh`

此指令碼使用 `tests/unit/test_tools.py` 中 BigQuery 工具的模擬 BQ 用戶端執行單元測試。

## 部署代理程式

可以使用下列指令將代理程式部署到 Vertex AI Agent Engine：

在 `.env` 中修改此項 -> `DISABLE_WEB_DRIVER=1`

```bash
python deployment/deploy.py --create
```

您也可以修改部署指令碼以符合您的使用案例。

## 自訂

如何自訂

* **修改對話流程：** 若要要求代理程式比較描述而非標題，您可以變更 `brand_search_optimization/sub_agents/search_results/prompt.py` 中的提示，具體來說，可以變更 `SEARCH_RESULT_AGENT_PROMPT` 下的 `<Gather Information>` 區段。
* **變更資料來源：** 可以透過變更 `.env` 檔案中的值，將 BigQuery 表格設定為指向某個表格。
* **變更網站：** 此處的範例網站是 Google Shopping，請以您自己的網站取代，並相應地修改任何程式碼。

### BigQuery 設定

#### 自動化

`sh deployment/run.sh` 會執行一個指令碼，使用範例資料填入 BigQuery 表格。它會在幕後呼叫 `python tools/bq_populate_data.py` 指令碼。

#### 資料集和表格權限

如果您想在非您擁有的 BigQuery 表格上執行代理程式，
請參閱[此處](./customization.md)的說明以授予必要的權限。

#### 手動步驟

檢查 `deployment/bq_data_setup.sql` 中的 SQL 查詢以手動新增資料。

## 疑難排解與常見問題

### BigQuery 資料不存在

這與 - 找不到資料集、在該位置找不到資料集、使用者沒有 BigQuery 資料集的權限有關。

錯誤：

```bash
google.api_core.exceptions.NotFound: 404 Not found: Dataset ...:products_data_agent was not found in location US; reason: notFound, message: Not found: Dataset ...:products_data_agent was not found in location US
```

修正：
確保您遵循「BigQuery 設定」區段。

### Selenium 問題

這與 Selenium / Webdriver 問題有關。

錯誤：

```bash
selenium.common.exceptions.SessionNotCreatedException: Message: session not created: probably user data directory is already in use, please specify a unique value for --user-data-dir argument, or don't use --user-data-dir
```

修正：移除資料目錄

```bash
rm -rf /tmp/selenium
```

### 代理程式流程問題

#### 已知問題

* 當網站強制執行機器人檢查且搜尋元素隱藏時，代理程式無法可靠地執行。
* 代理程式未建議下一步 - 這發生在關鍵字尋找階段之後。在此情況下，要求代理程式搜尋排名靠前的關鍵字。例如：「您可以搜尋關鍵字嗎？」或更明確地說「將我轉移到網頁瀏覽器代理程式」。
* 代理程式再次要求關鍵字 - 例如：「好的，我將前往 XYZ.com。您想在 XYZ 上搜尋哪個關鍵字？」。請再次提供關鍵字。