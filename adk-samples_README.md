# Agent Development Kit (ADK) Samples

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

<img src="https://github.com/google/adk-docs/blob/main/docs/assets/agent-development-kit.png" alt="Agent Development Kit Logo" width="150">

Welcome to the Sample Agents repository! This collection provides ready-to-use agents built on top of the [Agent Development Kit](https://github.com/google/adk-python), designed to accelerate your development process.  These agents cover a range of common use cases and complexities, from simple conversational bots to complex multi-agent workflows.

## ✨ What are Sample Agents?

A Sample Agent is a functional starting point for a foundational agent designed for common application scenarios. It comes pre-packaged with core logic (like different agents using different tools, evaluation, human in the loop) relevant to a specific use case or industry. While functional, a Sample Agent typically requires customization (e.g., adjusting specific responses or integrating with external systems) to be fully operational. Each agent includes instructions on how it can be customized.

## 🚀 Getting Started

Follow these steps to set up and run the sample agents:

1.  **Prerequisites:**
    *   **Install the ADK Samples:** Ensure you have the Agent Development Kit installed and configured. Follow the [ADK Installation Guide](https://google.github.io/adk-docs/get-started/installation/).
    *   **Set Up Environment Variables:** Each agent example relies on a `.env` file for configuration (like API keys, Google Cloud project IDs, and location). This keeps secrets out of the code.
        *   You will need to create a `.env` file in each agent's directory you wish to run (usually by copying the provided `.env.example`).
        *   Setting up these variables, especially obtaining Google Cloud credentials, requires careful steps. Refer to the **Environment Setup** section in the [ADK Installation Guide](https://google.github.io/adk-docs/get-started/installation/) for detailed instructions.
    *   **Google Cloud Project (Recommended):** While some agents might run locally with just an API key, most leverage Google Cloud services like Vertex AI and BigQuery. A configured Google Cloud project is highly recommended. See the [ADK Quickstart](https://google.github.io/adk-docs/get-started/quickstart/) for setup details.


2.  **Clone this repository:**
You can install the ADK samples via cloning it from the public repository by
    ```bash
    git clone https://github.com/google/adk-samples.git
    cd adk-samples
    ```

3.  **Explore the Agents:**

*   Navigate to the `agents/` directory.
*   The `agents/README.md` provides an overview and categorization of the available agents.
*   Browse the subdirectories. Each contains a specific sample agent with its own `README.md`.

4.  **Run an Agent:**
    *   Choose an agent from the `agents/` directory.
    *   Navigate into that agent's specific directory (e.g., `cd agents/llm-auditor`).
    *   Follow the instructions in *that agent's* `README.md` file for specific setup (like installing dependencies via `poetry install`) and running the agent.

    Browse the folders in this repository. Each agent and tool have its own `README.md` file with detailed instructions.

**Notes:**
* These agents have been built and tested using [Google models](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models) on Vertex AI. You can test these samples with other models as well. Please refer to [ADK Tutorials](https://google.github.io/adk-docs/agents/models/) to use other models for these samples. 

## 🧱 Repository Structure
```bash
.
├── agents                  # Contains individual agent samples 
│   ├── agent1              # Specific agent directory
│   │   └── README.md       # Agent-specific instructions    
│   ├── agent2
│   │   └── README.md
│   ├── ...   
│   └── README.md           # Overview and categorization of agents
└── README.md               # This file (Repository overview)
```

## ℹ️ Getting help

If you have any questions or if you found any problems with this repository, please report through [GitHub issues]( https://github.com/google/adk-samples/issues).

## 🤝 Contributing

We welcome contributions from the community! Whether it's bug reports, feature requests, documentation improvements, or code contributions, please see our [**Contributing Guidelines**](https://github.com/google/adk-samples/blob/main/CONTRIBUTING.md) to get started.

## 📄 License

This project is licensed under the Apache 2.0 License - see the [LICENSE](https://github.com/google/adk-samples/blob/main/LICENSE) file for details.

## Disclaimers

This is not an officially supported Google product. This project is not eligible for the [Google Open Source Software Vulnerability Rewards Program](https://bughunters.google.com/open-source-security).

This project is intended for demonstration purposes only. It is not intended for use in a production environment.