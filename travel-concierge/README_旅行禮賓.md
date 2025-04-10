# 旅行禮賓

此範例展示如何使用 Agent Development Kit (ADK) 為旅行者提供全新的使用者體驗。一群代理程式模仿個人旅行禮賓的概念，滿足旅行者的需求：從旅行構思、規劃和預訂，到為旅行做準備、在旅途中協助從 A 點到 B 點，同時充當資訊豐富的嚮導。

此範例包含使用 ADK 支援工具的說明，例如 Google Places API、Google Search Grounding 和 MCP。

## 概觀

旅行者的體驗可分為兩個階段：預訂前和預訂後。在此範例中，每個階段都涉及多個專業代理程式協同工作，以提供禮賓體驗。

在預訂前階段，會建構不同的代理程式來協助旅行者尋找度假靈感、規劃活動、尋找航班和飯店，並協助處理預訂付款。預訂前階段以旅行行程告終。

在預訂後階段，根據具體的行程，另一組代理程式會在旅行前、旅行中和旅行後支援旅行者的需求。例如，行前代理程式會檢查簽證和醫療要求、旅遊建議和風暴狀態。行程中代理程式會監控預訂的任何變更，並有當日代理程式協助旅行者在旅途中從 A 點到達 B 點。行程後代理程式則協助收集意見回饋並識別未來旅行計劃的其他偏好。


## 代理程式詳細資訊
旅行禮賓的主要功能包括：

| 功能 | 說明 |
| --- | --- |
| **互動類型：** | 對話式 |
| **複雜度：**  | 進階 |
| **代理程式類型：**  | 多代理程式 |
| **元件：**  | 工具、代理程式工具、記憶體 |
| **垂直領域：**  | 旅遊 |

請參閱 [MCP](#mcp) 部分，以了解使用 Airbnb 的 MCP 搜尋工具的範例。

### 代理程式架構
旅行禮賓代理程式架構

<img src="travel-concierge-arch.png" alt="旅行禮賓的多代理程式架構" width="800"/>

### 元件詳細資訊

擴充上述的「關鍵元件」。
*   **代理程式：**
    * `inspiration_agent` - 與使用者互動，提供目的地和活動建議，激發使用者選擇其中之一。
    * `planning_agent` - 給定目的地、開始日期和持續時間，規劃代理程式協助使用者選擇航班、座位和飯店（模擬），然後產生包含活動的行程。
    * `booking_agent` - 給定行程，預訂代理程式將協助處理行程中需要付款的項目。
    * `pre_trip_agent` - 預計在旅行開始前定期調用；此代理程式根據出發地、目的地和使用者的國籍擷取相關的旅行資訊。
    * `in_trip_agent`- 預計在旅行期間頻繁調用。此代理程式提供三種服務：監控預訂的任何變更（模擬）、充當資訊豐富的嚮導，並提供交通協助。
    * `post_trip_agent` - 在此範例中，行程後代理程式會詢問旅行者的體驗，並嘗試根據行程提取和儲存他們的各種偏好，以便這些資訊在未來的互動中發揮作用。
*   **工具：**
    * `map_tool` - 擷取經緯度；使用 Google Map API 對地址進行地理編碼。
    * `memorize` - 一個函數，用於記住對話中對旅行規劃和提供行程中支援很重要的資訊。
*   **代理程式工具：**
    * `google_search_grounding` - 在範例中用於行前資訊收集，例如簽證、醫療、旅遊建議等。
    * `what_to_pack` - 根據出發地和目的地建議打包物品。
    * `place_agent` - 推薦目的地。
    * `poi_agent` - 根據目的地建議活動。
    * `itinerary_agent` - 由 `planning_agent` 調用，以根據 pydantic 結構描述完整建構和表示 JSON 格式的行程。
    * `day_of_agent` - 由 `in_trip_agent` 調用，以提供當天和當下的行程中交通資訊，從 A 點到 B 點。使用動態指令實作。
    * `flight_search_agent` - 模擬航班搜尋，給定出發地、目的地、去程和回程日期。
    * `flight_seat_selection_agent` - 模擬座位選擇，部分座位不可用。
    * `hotel_search_agent` - 模擬飯店選擇，給定目的地、去程和回程日期。
    * `hotel_room_selection_agent` - 模擬飯店房間選擇。
    * `confirm_reservation_agent` - 模擬預訂。
    * `payment_choice` - 模擬付款選擇，Apple Pay 會失敗，Google Pay 和信用卡會成功。
    * `payment_agent` - 模擬付款處理。
*   **記憶體：**
    * 此範例中的所有代理程式和工具都使用 Agent Development Kit 的內部會話狀態作為記憶體。
    * 會話狀態用於儲存行程等資訊，以及代理程式工具的臨時回應。
    * 有許多預製的行程可以載入以進行測試運行。請參閱下方的「執行代理程式」以了解如何執行它們。

## 設定與安裝

### 資料夾結構
```
.
├── README.md
├── travel-concierge-arch.png
├── pyproject.toml
├── travel_concierge/
│   ├── shared_libraries/
│   ├── tools/
│   └── sub_agents/
│       ├── inspiration/
│       ├── planning/
│       ├── booking/
│       ├── pre_trip/
│       ├── in_trip/
│       └── post_trip/
├── tests/
│   └── unit/
├── eval/
│   └── data/
└── deployment/
```

### 先決條件

- Python 3.11+
- Google Cloud 專案（用於 Vertex AI 整合）
- [Google Maps Platform Places API](https://developers.google.com/maps/documentation/places/web-service/get-api-key) 的 API 金鑰
- Google Agent Development Kit 1.0+
- Poetry：按照官方 Poetry [網站](https://python-poetry.org/docs/) 上的說明安裝 Poetry

### 安裝

1.  複製儲存庫：

    ```bash
    git clone https://github.com/google/adk-samples.git
    cd adk-samples/agents/travel-concierge
    ```
    注意：從這裡開始，除非另有說明，否則所有命令列指令都應在 `travel-concierge/` 目錄下執行。

2.  使用 Poetry 或 pip 安裝依賴項：

    ```bash
    poetry install
    ```

3.  設定 Google Cloud 憑證：

    否則：
    - 在頂層目錄 `travel-concierge/` 中，透過複製 `.env.example` 來建立 `.env` 檔案。
    - 設定以下環境變數。
    - 若要使用 Vertex，請確保您已在專案中啟用 Vertex AI API。
    ```
    # 選擇模型後端：0 -> ML Dev，1 -> Vertex
    GOOGLE_GENAI_USE_VERTEXAI=1
    # ML Dev 後端設定，當 GOOGLE_GENAI_USE_VERTEXAI=0 時，如果使用 Vertex 則忽略。
    # GOOGLE_API_KEY=YOUR_VALUE_HERE

    # Vertex 後端設定
    GOOGLE_CLOUD_PROJECT=__YOUR_CLOUD_PROJECT_ID__
    GOOGLE_CLOUD_LOCATION=us-central1

    # Places API
    GOOGLE_PLACES_API_KEY=__YOUR_API_KEY_HERE__

    # GCS 儲存桶名稱 - 用於 Agent Engine 部署測試
    GOOGLE_CLOUD_STORAGE_BUCKET=YOUR_BUCKET_NAME_HERE

    # 範例情境路徑 - 預設為空行程
    # 這將在首次使用者互動時載入。
    #
    # 取消註解以下兩者之一，或建立您自己的。
    #
    # TRAVEL_CONCIERGE_SCENARIO=eval/itinerary_seattle_example.json
    TRAVEL_CONCIERGE_SCENARIO=eval/itinerary_empty_default.json
    ```

4. 驗證您的 GCloud 帳戶。
    ```bash
    gcloud auth application-default login
    ```

5. 啟動由 Poetry 設定的虛擬環境，執行：
    ```bash
    eval $(poetry env activate)
    (travel-concierge-py3.12) $ # 進入虛擬環境
    ```
    每當您開啟新的 shell 時，請重複此命令，然後再執行此 README 中的命令。

## 執行代理程式

### 使用 `adk`

ADK 提供了在本機啟動代理程式並與其互動的便利方法。
您可以使用 CLI 與代理程式交談：

```bash
# 在 travel-concierge 目錄下：
adk run travel_concierge
```

或透過其 Web 介面：
```bash
# 在 travel-concierge 目錄下：
adk web
```

這將在您的機器上啟動一個本地 Web 伺服器。您可以開啟 URL，在左上角的下拉式選單中選擇 "travel_concierge"，
右側將出現一個聊天機器人介面。

對話最初是空白的。有關禮賓互動的大綱，請參閱 [範例代理程式互動](#範例代理程式互動) 部分。

以下是一些可以嘗試的內容：
* "需要一些美洲的目的地建議"
* 與代理程式互動一段時間後，您可以問："繼續規劃"。


### 程式化存取

以下是使用 Python 將代理程式作為伺服器進行互動的範例。
在 travel-concierge 目錄下嘗試：

首先，為 travel_concierge 套件建立一個快速開發 API 伺服器。
```bash
adk api_server travel_concierge
```
這將在 http://127.0.0.1:8000 啟動一個 fastapi 伺服器。
您可以在 http://127.0.0.1:8000/docs 存取其 API 文件。

以下是一個僅呼叫伺服器兩次的範例客戶端：
```bash
python tests/programmatic_example.py
```

您可能會注意到有處理函數回應的程式碼。我們將在下面的 [GUI](#gui) 部分重新討論這一點。


### 範例代理程式互動

提供了兩個範例會話來說明旅行禮賓如何運作。
- 從靈感到最終預訂秘魯之旅的旅行規劃 ([`tests/pre_booking_sample.md`](tests/pre_booking_sample.md))。
- 前往西雅圖短途旅行的行程中體驗，使用工具模擬時間的流逝 ([`tests/post_booking_sample.md`](tests/post_booking_sample.md))。

### 值得嘗試

與其一次與禮賓互動一次，不如嘗試給它完整的指令，包括決策標準，然後觀察它的工作情況，例如：

  *"尋找 4 月 20 日從 JFK 飛往倫敦的航班，為期 4 天。選擇任何航班和任何座位；還有任何飯店和房型。確保為兩個航班都選擇座位。繼續代表我行動，無需我的輸入，直到您選擇了所有內容，在產生行程之前與我確認。"*

在沒有針對此類用法進行特別優化的情況下，這群代理程式似乎能夠在很少輸入的情況下代表您自行運作。


## 執行測試

若要執行說明性測試和評估，請安裝額外的依賴項並執行 pytest：

```
poetry install --with dev
pytest
```

不同的測試也可以分開執行：

若要執行單元測試，只需檢查所有代理程式和工具是否回應：
```
pytest tests
```

若要執行代理程式軌跡測試：
```
pytest eval
```

## 部署代理程式

若要將代理程式部署到 Vertex AI Agent Engine，請在 `travel-concierge` 下執行以下命令：

```bash
poetry install --with deployment
python deployment/deploy.py --create
```
當此命令返回時，如果成功，它將列印一個 AgentEngine 資源
ID，如下所示：
```
projects/************/locations/us-central1/reasoningEngines/7737333693403889664
```

若要快速測試代理程式是否已成功部署，
執行以下命令，與代理程式進行一次互動 "尋找美洲周圍的靈感"：
```bash
python deployment/deploy.py --quicktest --resource_id=<RESOURCE_ID>
```
這將返回一個 JSON 負載流，表示已部署的代理程式功能正常。

若要刪除代理程式，請執行以下命令（使用先前返回的資源 ID）：
```bash
python3 deployment/deploy.py --delete --resource_id=<RESOURCE_ID>
```

## 應用程式開發

### 回呼和初始狀態

此示範中的 root_agent 目前註冊了一個 `before_agent_callback`，用於將初始狀態（例如使用者偏好和行程）從檔案載入到會話狀態以進行互動。這樣做的主要原因是減少必要的設定量，並且可以輕鬆使用 adk UI。

在實際的應用程式情境中，可以在建立新的 `Session` 時包含初始狀態，從而滿足使用者偏好和其他資訊很可能從外部資料庫載入的使用案例。

### 記憶體 vs 狀態

在此範例中，我們使用會話狀態作為禮賓的記憶體，以儲存行程以及中間代理程式/工具/使用者偏好回應。在實際的應用程式情境中，使用者設定檔的來源應為外部資料庫，並且
從工具到會話狀態的相互寫入應額外持久化（作為寫穿）到專用於使用者設定檔和行程的外部資料庫。

### MCP

包含一個使用 Airbnb 的 MCP 伺服器的範例。ADK 支援 MCP 並提供多個 MCP 工具。
此範例將 Airbnb 搜尋和列表 MCP 工具附加到 `planning_agent`，並要求禮賓只需在給定特定日期的情况下尋找 airbnb。禮賓會將請求轉發給規劃代理程式，後者將呼叫 Airbnb 搜尋 MCP 工具。

若要嘗試此範例，請先從 Node.js [網站](https://nodejs.org/en/download) 設定 nodejs 和 npx。

確保：
```
$ which node
/Users/USERNAME/.nvm/versions/node/v22.14.0/bin/node

$ which npx
/Users/USERNAME/.nvm/versions/node/v22.14.0/bin/npx
```

然後，在 `travel-concierge/' 目錄下，使用以下命令執行測試：
```
python -m tests.mcp_abnb
```

您將在控制台上看到類似以下的輸出：
```
[user]: 幫我找一個聖地牙哥的 airbnb，4 月 9 日到 4 月 13 日，不需要航班或行程。無需確認，只需返回 5 個選擇，記得包含網址。

( 設定代理程式和工具 )

Server started with options: ignore-robots-txt
Airbnb MCP Server running on stdio

Inserting Airbnb MCP tools into Travel-Concierge...
...
FOUND planning_agent

( Execute: Runner.run_async() )

[root_agent]: transfer_to_agent( {"agent_name": "planning_agent"} )
...
[planning_agent]: airbnb_search( {"checkout": "2025-04-13", "location": "San Diego", "checkin": "2025-04-09"} )

[planning_agent]: airbnb_search responds -> {
  "searchUrl": "https://www.airbnb.com/s/San%20Diego/homes?checkin=2025-04-09&checkout=2025-04-13&adults=1&children=0&infants=0&pets=0",
  "searchResults": [
    {
      "url": "https://www.airbnb.com/rooms/24669593",
      "listing": {
        "id": "24669593",
        "title": "Room in San Diego",
        "coordinate": {
          "latitude": 32.82952,
          "longitude": -117.22201
        },
        "structuredContent": {
          "mapCategoryInfo": "Stay with Stacy, Hosting for 7 years"
        }
      },
      "avgRatingA11yLabel": "4.91 out of 5 average rating,  211 reviews",
      "listingParamOverrides": {
        "categoryTag": "Tag:8678",
        "photoId": "1626723618",
        "amenities": ""
      },
      "structuredDisplayPrice": {
        "primaryLine": {
          "accessibilityLabel": "$9,274 TWD for 4 nights"
        },
        "explanationData": {
          "title": "Price details",
          "priceDetails": "$2,319 TWD x 4 nights: $9,274 TWD"
        }
      }
    },
    ...
    ...
  ]
}

[planning_agent]: 這是您從 4 月 9 日到 4 月 13 日在聖地牙哥旅行的 5 個 Airbnb 選項，包括網址：

1.  聖地牙哥的房間：[https://www.airbnb.com/rooms/24669593](https://www.airbnb.com/rooms/24669593)
2.  聖地牙哥的房間：[https://www.airbnb.com/rooms/5360158](https://www.airbnb.com/rooms/5360158)
3.  聖地牙哥的房間：[https://www.airbnb.com/rooms/1374944285472373029](https://www.airbnb.com/rooms/1374944285472373029)
4.  聖地牙哥的公寓：[https://www.airbnb.com/rooms/808814447273523115](https://www.airbnb.com/rooms/808814447273523115)
5.  聖地牙哥的房間：[https://www.airbnb.com/rooms/53010806](https://www.airbnb.com/rooms/53010806)
```

### GUI

典型的終端使用者將透過 GUI 而非純文字與代理程式互動。前端禮賓應用程式可能會以圖形方式和/或使用豐富媒體呈現多種代理程式回應，例如：
- 目的地建議以卡片輪播形式呈現，
- 地圖上的興趣點/方向，
- 可展開的影片、圖片、連結。
- 航班和飯店選擇以帶有標誌的列表形式呈現，
- 在座位圖上選擇航班座位，
- 可點擊的預設回應。

其中許多可以透過 ADK 的事件來實現。這是因為：
- 所有函數呼叫和函數回應都由會話執行器報告為事件。
- 在此 travel-concierge 範例中，多個子代理程式和工具使用明確的 pydantic 結構描述和受控生成來產生 JSON 回應。這些代理程式是：地點代理程式（用於目的地）、poi 代理程式（用於 poi 和活動）、航班和飯店選擇代理程式、座位和房間選擇代理程式以及行程。
- 當會話執行器服務被包裝為伺服器端點時，攜帶這些 JSON 負載的事件序列可以流式傳輸到應用程式。
- 當應用程式透過其來源代理程式識別負載結構描述時，它可以相應地呈現負載。

若要了解如何使用事件、代理程式和工具回應，請開啟檔案 [`tests/programmatic_example.py`](tests/programmatic_example.py)。

使用以下命令執行測試客戶端程式碼：
```
python tests/programmatic_example.py
```

您將獲得類似以下的輸出：
```json
[user]: "給我一些關於馬爾地夫的靈感"

...

[root_agent]: transfer_to_agent( {"agent_name": "inspiration_agent"} )

...

[inspiration_agent]: place_agent responds -> {
  "id": "af-be786618-b60b-45ee-a801-c40fd6811e60",
  "name": "place_agent",
  "response": {
    "places": [
      {
        "name": "馬累",
        "country": "馬爾地夫",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Male%2C_Maldives_panorama_2016.jpg/1280px-Male%2C_Maldives_panorama_2016.jpg",
        "highlights": "充滿活力的首都，提供繁華的市場、歷史悠久的清真寺，並可一窺當地馬爾地夫人的生活。",
        "rating": "4.2"
      },
      {
        "name": "芭環礁",
        "country": "馬爾地夫",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Baa_Atoll_Maldives.jpg/1280px-Baa_Atoll_Maldives.jpg",
        "highlights": "聯合國教科文組織生物圈保護區，以其豐富的海洋生物多樣性而聞名，包括蝠鱝和鯨鯊，非常適合浮潛和潛水。",
        "rating": "4.8"
      },
      {
        "name": "阿杜環礁",
        "country": "馬爾地夫",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Addu_Atoll_Maldives.jpg/1280px-Addu_Atoll_Maldives.jpg",
        "highlights": "最南端的環礁，以其獨特的赤道植被、二戰歷史遺址和擁有各種珊瑚礁的絕佳潛水點而聞名。",
        "rating": "4.5"
      }
    ]
  }
}

[app]: 呈現目的地輪播

[inspiration_agent]: 馬爾地夫是一個很棒的目的地！我看到三個不錯的選擇：

1.  **馬累：** 首都，您可以在這裡體驗當地生活、市場和清真寺。
2.  **芭環礁：** 聯合國教科文組織生物圈保護區，非常適合浮潛和潛水，有蝠鱝和鯨鯊。
3.  **阿杜環礁：** 最南端的環礁，提供獨特的植被、二戰歷史和多樣化的珊瑚礁供潛水。

這些目的地中有沒有哪個聽起來很有趣？我可以為您提供您所選目的地的一些活動。

[user]: "建議一些芭環礁周圍的活動"

...

```

在事件從執行代理程式的伺服器傳遞到應用程式前端的環境中，應用程式可以使用此範例中的方法來解析和識別正在傳送哪個負載，並選擇最合適的負載呈現器/處理器。

## 自訂

以下是一些關於如何重用禮賓並使其成為您自己的想法。

### 載入預製行程以演示行程中流程
- 預設情況下，會從 `eval/itinerary_empty_default.json` 載入 user_profile 和空行程。
- 若要指定要載入的不同檔案，例如西雅圖範例 `eval/itinerary_seattle_example.json`：
  - 在 `.env` 中將環境變數 `TRAVEL_CONCIERGE_SCENARIO` 設定為 `eval/itinerary_seattle_example.json`。
  - 然後重新啟動 `adk web` 並載入旅行禮賓。
- 當您開始與代理程式互動時，狀態將被載入。
- 當您在 GUI 中選擇「狀態」時，您可以看到載入的使用者設定檔和行程。


### 為演示製作您自己的預製行程

- 行程結構描述在 types.py 中定義。
- 複製 itinerary_seattle_example.json 並按照結構描述製作您自己的 `itinerary`。
- 使用上述步驟載入和測試您的新行程。
- 對於 `user_profile` 字典：
  - `passport_nationality` 和 `home` 是必填欄位，僅修改 `address` 和 `local_prefer_mode`。
  - 您可以修改/新增額外的設定檔欄位到


### 與外部 API 整合

此範例中有許多增強、自訂和整合的機會：
- 連接到真實的航班/座位選擇系統
- 連接到真實的飯店/房間選擇系統
- 使用外部記憶體持久化服務或資料庫，而不是會話狀態
- 在 day_of 代理程式中使用 Google Maps [Route API](https://developers.google.com/maps/documentation/routes)。
- 連接到外部 API 以獲取簽證/醫療/旅遊建議和 NOAA 風暴資訊，而不是使用 Google Search Grounding。


### 優化代理程式

以下只是一些初步的想法：
- 更複雜的行程和活動規劃代理程式；例如，目前代理程式不處理中途停留的航班。
- 更好的會計 - 計算航班、飯店和其他費用的準確性。
- 一個不那麼單調乏味且更有效率的預訂代理程式
- 對於行前和行程中代理程式，有機會動態調整行程並解決旅行異常情況


## 疑難排解

與代理程式互動時偶爾會發生以下情況：
- 「格式錯誤」的函數呼叫或回應，或 pydantic 錯誤 - 發生這種情況時，只需告訴代理程式「再試一次」。
- 如果代理程式嘗試呼叫不存在的工具，請告訴代理程式這是「錯誤的工具，再試一次」，代理程式通常能夠自我修正。
- 同樣，如果您等待了一段時間並且代理程式在執行一系列操作的過程中停止了，請詢問代理程式「接下來是什麼」以推動它前進。

這些情況偶爾會發生，很可能是由於 JSON 回應的變化，需要對提示和生成參數進行更嚴格的實驗才能獲得更穩定的結果。在應用程式中，這些重試也可以作為異常處理的一部分內建到應用程式中。