# LLM 審計師

此代理程式作為一個自動化的事實查核層，專門設計用於評估和增強大型語言模型 (LLM) 所生成回應的事實基礎。其主要作用是透過系統性地分析 LLM 輸出與真實世界資訊的對比來提高其可靠性；它透過識別文本中可驗證的聲明、利用網路搜尋及其內部知識來確定其準確性、產生詳細的調查結果報告，並可選擇性地重寫原始回應以糾正任何發現的不準確之處來實現此目標。

## 概觀

此代理程式評估並改進 LLM 生成回應的事實基礎。其主要目的是作為一個自動化的事實查核層，分析 LLM 的答案與真實世界資訊，以提高可靠性。

*   識別並分離 LLM 生成文本中的具體、可驗證的陳述。
*   使用網路搜尋工具和其訓練所獲得的知識來確定聲明的準確性。
*   產生清晰的明細，列出已識別的聲明及其驗證狀態。
*   可選擇性地根據驗證結果重寫原始回應以糾正不準確之處。

此範例代理程式讓使用者能夠查詢 LLM，代理程式則透過提取聲明、利用搜尋工具進行驗證、產生審計報告，並可選擇性地重寫回應來審核相應的答案。

## 代理程式詳細資訊

LLM 審計師的主要功能包括：

| 功能           | 描述                               |
| -------------- | ---------------------------------- |
| **互動類型**   | 工作流程 (Workflow)                |
| **複雜度**     | 簡單 (Easy)                        |
| **代理程式類型** | 多代理程式 (Multi Agent)           |
| **元件**       | 工具：內建 Google 搜尋             |
| **垂直領域**   | 水平 (Horizontal)                  |

### 代理程式架構：

此圖顯示了用於實作此工作流程的代理程式和工具的詳細架構。
<img src="llm_auditor_architecture.png" alt="LLM 審計師架構" width="800"/>

## 設定與安裝

1.  **先決條件**

    *   Python 3.11+
    *   Poetry
        *   用於依賴管理和打包。請遵循官方 [Poetry 網站](https://python-poetry.org/docs/) 上的說明進行安裝。
        ```bash
        pip install poetry
        ```
    *   Google Cloud Platform 上的專案
    *   Google Cloud CLI
        *   有關安裝，請遵循官方 [Google Cloud 網站](https://cloud.google.com/sdk/docs/install) 上的說明。

2.  **安裝**

    ```bash
    # 複製此儲存庫。
    git clone https://github.com/google/adk-samples.git
    cd agents/llm-auditor
    # 安裝套件和依賴項。
    poetry install
    ```

3.  **設定**

    *   設定 Google Cloud 憑證。

        *   您可以在 shell 中設定以下環境變數，或改用 `.env` 檔案。

        ```bash
        export GOOGLE_GENAI_USE_VERTEXAI=true
        export GOOGLE_CLOUD_PROJECT=<您的專案 ID>
        export GOOGLE_CLOUD_LOCATION=<您的專案位置>
        export GOOGLE_CLOUD_STORAGE_BUCKET=<您的儲存空間儲存桶>  # 僅在 Agent Engine 上部署時需要
        ```

    *   驗證您的 GCloud 帳戶。

        ```bash
        gcloud auth application-default login
        gcloud auth application-default set-quota-project $GOOGLE_CLOUD_PROJECT
        ```

## 執行代理程式

**使用 `adk`**

ADK 提供了在本機啟動代理程式並與之互動的便利方法。您可以使用 CLI 與代理程式對話：

```bash
adk run llm_auditor
```

或在網頁介面上：

```bash
adk web
```

`adk web` 指令將在您的機器上啟動一個網頁伺服器並印出 URL。您可以開啟該 URL，在左上角的下拉式選單中選擇 "llm_auditor"，右側將出現一個聊天機器人介面。對話最初是空白的。以下是一些您可以要求 LLM 審計師驗證的範例請求：

*   `仔細檢查這個：地球比火星離太陽更遠。`
*   `問：為什麼藍莓是藍色的？答：因為藍莓的表皮有色素。`

這些請求的回應範例顯示在下方的 [範例互動](#範例互動) 部分。

**程式化存取**

以下是使用 Python 與代理程式互動的範例：

```python
import dotenv
dotenv.load_dotenv()  # 如果您已匯出環境變數，則可跳過。
from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent
from llm_auditor.agent import root_agent

user_input = "仔細檢查這個：地球比火星離太陽更遠。"

runner = InMemoryRunner(agent=root_agent)
session = runner.session_service.create_session(
    app_name=runner.app_name, user_id="test_user"
)
content = UserContent(parts=[Part(text=user_input)])
for event in runner.run(
    user_id=session.user_id, session_id=session.id, new_message=content
):
    for part in event.content.parts:
        print(part.text)
```

您也可以利用 `google.adk.Runner` 來對互動會話等進行更精細的控制，或將代理程式包裝在 `vertexai.preview.reasoning_engines.AdkApp` 中。

### 範例互動

以下是與 LLM 審計師互動的範例。請注意，代理程式的確切輸出每次可能會有所不同。

```
使用者：仔細檢查這個：地球比火星離太陽更遠。

[critic_agent]：好的，我將仔細檢查這個陳述：「地球比火星離太陽更遠。」

**步驟 1：識別聲明 (CLAIMS)**

答案包含一個聲明：

* 聲明 1：地球比火星離太陽更遠。

**步驟 2：驗證每個聲明 (CLAIM)**

* 聲明 1：地球比火星離太陽更遠。
    * 背景：這是關於地球和火星相對於太陽距離的直接事實陳述。
    * 外部來源：我將使用 Google 搜尋來檢查地球和火星距離太陽的平均距離。
    * 結論：**不準確**。
    * 理由：根據搜尋結果，地球距離太陽的平均距離約為 1.5 億公里 [2, 3, 6, 9]，而火星距離太陽的平均距離約為 2.28 億公里 [1, 4, 5, 8, 10]。因此，火星比地球離太陽更遠，這與該聲明相矛盾。

**步驟 3：提供整體評估**

    * 整體結論：不準確
    * 整體理由：答案中提出的單一聲明根據廣泛可用的天文數據證明是錯誤的。因此，整個答案是不正確的。

以下是我的驗證結果摘要：

* 聲明：地球比火星離太陽更遠。
    * 答案文本中的部分：「地球比火星離太陽更遠。」
    * 結論：不準確
    * 理由：地球距離太陽的平均距離約為 1.5 億公里，而火星距離太陽的平均距離約為 2.28 億公里。因此，火星比地球離太陽更遠。

參考資料：

<為清晰起見省略>

[reviser_agent]：火星比地球離太陽更遠。
```

```
使用者：問：為什麼藍莓是藍色的？答：因為藍莓的表皮有色素。

[critic_agent]：好的，我將分析問題「為什麼藍莓是藍色的？」的答案，以驗證其準確性和完整性。

**步驟 1：識別聲明 (CLAIMS)**

我在答案中識別出以下聲明：

*   聲明 1：藍莓是藍色的，因為它們的表皮有色素。

**步驟 2：驗證每個聲明 (CLAIM)**

現在，我將驗證已識別的聲明。

*   考慮背景：問題詢問藍莓藍色的原因。
*   查閱外部來源：我將使用 Google 搜尋來查找有關造成藍莓藍色的色素的資訊。
*   確定結論 (VERDICT)：

    *   聲明 1：藍莓是藍色的，因為它們的表皮有色素。
        最初的答案部分正確但不完整。雖然藍莓的表皮確實含有色素，特別是花青素 [2, 4, 6, 8, 9]，但我們感知的藍色主要是由於果實表面的一層蠟質塗層散射藍光所致 [1, 2, 3, 5, 10, 11]。下面的色素實際上是深紅色的 [1, 3, 5, 10]。

*   結論：不準確。答案並非完全錯誤，因為藍莓的表皮確實含有色素。然而，它具有誤導性，因為它將藍色完全歸因於色素，忽略了蠟質塗層及其光散射特性的關鍵作用。

**步驟 3：提供整體評估**

*   整體結論：不準確
*   整體理由：提供的答案雖然提到了色素，但未能解釋藍莓藍色的主要原因，即散射藍光的蠟質塗層。因此，答案具有誤導性且不準確。

參考資料：

<為清晰起見省略>

[reviser_agent]：藍莓之所以是藍色，是因為它們表皮上的蠟質塗層會散射藍光。它們的表皮也含有色素。
```

## 執行測試

若要執行測試和評估，請安裝額外的依賴項：

```bash
poetry install --with dev
```

然後可以從 `llm-auditor` 目錄使用 `pytest` 模組執行測試和評估：

```bash
python3 -m pytest tests
python3 -m pytest eval
```

`tests` 在範例請求上執行代理程式，並確保每個元件都能正常運作。`eval` 是如何使用 ADK 中的 `AgentEvaluator` 評估代理程式的示範。它向代理程式發送幾個請求，並期望代理程式的回應與預先定義的回應合理地匹配。


## 部署

LLM 審計師可以使用以下指令部署到 Vertex AI Agent Engine：

```bash
poetry install --with deployment
python3 deployment/deploy.py --create
```

部署完成後，它將印出一行類似這樣的內容：

```
已建立遠端代理程式：projects/<專案編號>/locations/<專案位置>/reasoningEngines/<代理程式引擎 ID>
```

如果您忘記了 AGENT_ENGINE_ID，可以使用以下指令列出現有的代理程式：

```bash
python3 deployment/deploy.py --list
```

輸出將類似於：

```
所有遠端代理程式：

123456789 ("llm_auditor")
- 建立時間：2025-04-09 08:22:36.179879+00:00
- 更新時間：2025-04-09 08:25:42.734584+00:00
```

您可以在 Python 中以程式化方式與已部署的代理程式互動：

```python
import dotenv
dotenv.load_dotenv()  # 如果您已匯出環境變數，則可跳過。
from vertexai import agent_engines

agent_engine_id = "代理程式引擎 ID"
user_input = "仔細檢查這個：地球比火星離太陽更遠。"

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

LLM 審計師可以進行自訂以更好地滿足您的需求。例如：

1.  **替換檢索機制：** 將 `critic` 子代理程式的預設 `built_in_google_search` 工具替換為針對您的資料來源量身定制的替代檢索工具。
2.  **自訂代理程式指令：** 修改指導 `critic` 和 `reviser` 子代理程式的提示。這使您可以引導它們的重點（例如，檢查特定的合規規則、確保特定的寫作風格）或改進它們的回饋和修訂格式。
3.  **實作迭代處理：** 將 LLM 審計師設定為迭代操作。回應可以由代理程式重複評估和重寫，而不是單次處理，直到達到預定的品質閾值。