# Agent Development Kit (ADK) 樣本

[![許可證](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

<img src="https://github.com/google/adk-docs/blob/main/docs/assets/agent-development-kit.png" alt="Agent Development Kit Logo" width="150">

歡迎來到樣本代理程式庫！這個集合提供了基於 [Agent Development Kit](https://github.com/google/adk-python) 構建的即用型代理程式，旨在加速您的開發過程。這些代理程式涵蓋了從簡單的對話機器人到複雜的多代理工作流程的各種常見用例和複雜性。

## ✨ 什麼是樣本代理程式？

樣本代理程式是一個針對常見應用場景設計的基礎代理程式的功能性起點。它預先打包了與特定用例或行業相關的核心邏輯（如不同代理程式使用不同的工具、評估、人機互動）。雖然功能性，但樣本代理程式通常需要定制（例如，調整特定響應或與外部系統整合）才能完全運作。每個代理程式都包括如何進行定制的說明。

## 🚀 開始使用

按照以下步驟設置和運行樣本代理程式：

1. **前提條件：**
   * **安裝 ADK 樣本：** 確保已安裝並配置了 Agent Development Kit。請參閱 [ADK 安裝指南](https://google.github.io/adk-docs/get-started/installation/)。
   * **設置環境變量：** 每個代理程式示例都依賴於 `.env` 文件進行配置（如 API 密鑰、Google Cloud 項目 ID 和位置）。這可以將秘密信息從代碼中分離出來。
       * 您需要在每個您希望運行的代理程式目錄中創建一個 `.env` 文件（通常通過複製提供的 `.env.example`）。
       * 設置這些變量，尤其是獲取 Google Cloud 憑證，需要仔細的步驟。請參閱 [ADK 安裝指南](https://google.github.io/adk-docs/get-started/installation/) 中的 **環境設置** 部分以獲取詳細說明。
   * **Google Cloud 項目（推薦）：** 雖然有些代理程式可能只需 API 密鑰即可在本地運行，但大多數利用了 Google Cloud 服務，如 Vertex AI 和 BigQuery。建議配置一個 Google Cloud 項目。請參閱 [ADK 快速入門](https://google.github.io/adk-docs/get-started/quickstart/) 以獲取設置詳情。

2. **克隆此存儲庫：**
   您可以通過克隆公共存儲庫來安裝 ADK 樣本：
   ```bash
   git clone https://github.com/google/adk-samples.git
   cd adk-samples
   ```

3. **探索代理程式：**

   * 導航到 `agents/` 目錄。
   * `agents/README.md` 提供了可用代理程式的概述和分類。
   * 瀏覽子目錄。每個子目錄包含一個特定的樣本代理程式及其自己的 `README.md`。

4. **運行代理程式：**
   * 從 `agents/` 目錄中選擇一個代理程式。
   * 進入該代理程式的特定目錄（例如，`cd agents/llm-auditor`）。
   * 按照該代理程式的 `README.md` 文件中的說明進行特定設置（如通過 `poetry install` 安裝依賴項）並運行代理程式。

   瀏覽此存儲庫中的文件夾。每個代理程式和工具都有自己的 `README.md` 文件，內含詳細說明。

**注意：**
* 這些代理程式是使用 [Google 模型](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models) 在 Vertex AI 上構建和測試的。您也可以使用其他模型來測試這些樣本。請參閱 [ADK 教程](https://google.github.io/adk-docs/agents/models/) 以使用其他模型進行這些樣本。

## 🧱 存儲庫結構
```bash
.
├── agents                  # 包含個別代理程式樣本 
│   ├── agent1              # 特定代理程式目錄
│   │   └── README.md       # 代理程式特定說明    
│   ├── agent2
│   │   └── README.md
│   ├── ...   
│   └── README.md           # 代理程式的概述和分類
└── README.md               # 本文件（存儲庫概述）
```

## ℹ️ 獲取幫助

如果您有任何問題或發現此存儲庫有任何問題，請通過 [GitHub 問題](https://github.com/google/adk-samples/issues) 報告。

## 🤝 貢獻

我們歡迎來自社區的貢獻！無論是錯誤報告、功能請求、文檔改進還是代碼貢獻，請參閱我們的 [**貢獻指南**]（https://github.com/google/adk-samples/blob/main/CONTRIBUTING.md）以開始。

## 📄 許可證

此項目在 Apache 2.0 許可證下許可 - 詳情請參閱 [LICENSE](https://github.com/google/adk-samples/blob/main/LICENSE) 文件。

## 免責聲明

這不是 Google 官方支持的產品。此項目不符合 [Google 開源軟件漏洞獎勵計劃](https://bughunters.google.com/open-source-security) 的資格。

此項目僅用於示範目的。不適用於生產環境。